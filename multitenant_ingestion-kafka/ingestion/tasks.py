from confluent_kafka import Producer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from django.conf import settings
import json

producer = Producer({'bootstrap.servers': settings.KAFKA_BROKER_URL})

def create_kafka_topic(topic_name):
    """Create Kafka topic if it doesn't exist"""
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=settings.KAFKA_BROKER_URL.split(','),
            client_id='admin_client'
        )
        
        topic_list = [NewTopic(
            name=topic_name,
            num_partitions=1,
            replication_factor=1
        )]
        
        admin_client.create_topics(topic_list, validate_only=False)
        print(f"✅ Created Kafka topic: {topic_name}")
    except TopicAlreadyExistsError:
        print(f"ℹ️ Topic {topic_name} already exists")
    except Exception as e:
        print(f"⚠️ Warning: Could not create topic {topic_name}: {e}")
    finally:
        try:
            admin_client.close()
        except:
            pass

def send_file_uploaded_event(tenant_id, file_key):
    data = {'tenant_id': tenant_id, 'file_key': file_key}
    create_kafka_topic(settings.KAFKA_TOPIC)
    producer.produce(settings.KAFKA_TOPIC, json.dumps(data).encode())
    producer.flush()

def send_failure_event(tenant_id, reason):
    data = {'tenant_id': tenant_id, 'error': reason}
    create_kafka_topic(settings.KAFKA_FAILURE_TOPIC)
    producer.produce(settings.KAFKA_FAILURE_TOPIC, json.dumps(data).encode())
    producer.flush()
