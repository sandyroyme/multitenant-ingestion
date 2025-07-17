# ingestion/management/commands/consume_kafka.py

import json
import time
from confluent_kafka import Consumer
from django.core.management.base import BaseCommand
from ingestion.business_logic import process_file
from ingestion.tasks import send_failure_event

class Command(BaseCommand):
    help = 'Consumes Kafka messages from file_uploaded topic'

    def handle(self, *args, **options):
        conf = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'django-consumer-group',
            'auto.offset.reset': 'earliest'
        }

        consumer = Consumer(conf)
        topic = 'file_uploaded'
        consumer.subscribe([topic])

        self.stdout.write(self.style.SUCCESS(f"✅ Listening to Kafka topic: {topic}"))

        while True:
            try:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                
                if msg.error():
                    self.stderr.write(f"❌ Kafka error: {msg.error()}")
                    continue

                # Process message with error handling
                self.process_message(consumer, msg)

            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING("👋 Stopping consumer..."))
                break
            except Exception as e:
                self.stderr.write(f"❌ Unexpected error in main loop: {e}")
                self.stderr.write(f"❌ Error type: {type(e)}")
                # Continue running despite the error
                time.sleep(5)  # Wait a bit before continuing
                continue

        consumer.close()
        self.stdout.write(self.style.SUCCESS("✅ Kafka consumer closed."))

    def process_message(self, consumer, msg):
        """Process a single message with comprehensive error handling"""
        data = None
        try:
            # Parse JSON message
            data = json.loads(msg.value().decode('utf-8'))
            self.stdout.write(self.style.NOTICE(f"📦 Received message: {json.dumps(data, indent=2)}"))
            
            # Process the file
            success, result = process_file(data['tenant_id'], data['file_key'])
            
            if success:
                # Commit the offset to mark message as processed
                consumer.commit(msg)
                self.stdout.write(self.style.SUCCESS(f"✅ Message processed and committed: {result}"))
            else:
                # Send failure event for processing failure
                send_failure_event(data['tenant_id'], result)
                # Commit anyway to avoid infinite retry
                consumer.commit(msg)
                self.stderr.write(f"❌ File processing failed: {result}")
            
        except json.JSONDecodeError as e:
            self.stderr.write(f"❌ JSON decode error: {e}")
            # Send failure event with unknown tenant
            send_failure_event('unknown', f"JSON decode error: {e}")
            # Commit anyway to avoid infinite retry
            consumer.commit(msg)
            
        except KeyError as e:
            self.stderr.write(f"❌ Missing key in message: {e}")
            tenant_id = data.get('tenant_id', 'unknown') if data else 'unknown'
            send_failure_event(tenant_id, f"Missing key in message: {e}")
            # Commit anyway to avoid infinite retry
            consumer.commit(msg)
            
        except Exception as e:
            self.stderr.write(f"❌ Error processing message: {e}")
            self.stderr.write(f"❌ Error type: {type(e)}")
            
            # Send failure event
            tenant_id = data.get('tenant_id', 'unknown') if data else 'unknown'
            send_failure_event(tenant_id, str(e))
            
            # Commit anyway to avoid infinite retry of failed messages
            consumer.commit(msg)
            
            # Log the error but don't stop the service
            self.stderr.write(f"⚠️ Message processing failed, but service continues running")
