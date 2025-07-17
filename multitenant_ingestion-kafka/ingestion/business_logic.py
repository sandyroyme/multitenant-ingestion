from ingestion.s3_utils import get_file_from_s3, delete_file_from_s3
from ingestion.models import DataRecord
import csv

def process_file(tenant_id, file_key):
    """Process file with comprehensive error handling - never raises exceptions"""
    print(f"Processing file: {file_key}")
    
    try:
        # Get file content from S3
        file_content = get_file_from_s3(file_key)
        
        # Check if it's an Excel file
        if file_key.endswith(('.xlsx', '.xls')):
            error_msg = f"Excel files (.xlsx/.xls) are not supported yet. Please convert to CSV format."
            print(f"❌ {error_msg}")
            return False, error_msg
        
        # Handle CSV files
        try:
            data = file_content.decode('utf-8').splitlines()
        except UnicodeDecodeError:
            # Try alternate encodings if UTF-8 fails
            try:
                data = file_content.decode('latin-1').splitlines()
            except UnicodeDecodeError:
                error_msg = f"Unable to decode file {file_key}. Please ensure it's a valid CSV file."
                print(f"❌ {error_msg}")
                return False, error_msg
        
        # Process CSV data
        reader = csv.DictReader(data)
        records_created = 0
        
        for row in reader:
            print(row)
            try:
                DataRecord.objects.create(
                    tenant_id=tenant_id, 
                    model=row.get('Model'), 
                    device_id=row.get('Device_id'), 
                    device_type=row.get('Device_Type'), 
                    manufacturer=row.get('Manufacturer'), 
                    approval_date=row.get('Approval_Date'), 
                    data=row
                )
                records_created += 1
            except Exception as e:
                print(f"⚠️ Failed to create record for row: {e}")
                # Continue processing other rows
                continue
        
        # Clean up file from S3
        try:
            delete_file_from_s3(file_key)
        except Exception as e:
            print(f"⚠️ Failed to delete file from S3: {e}")
            # Don't fail the entire process if cleanup fails
        
        print(f"✅ Successfully processed {file_key} for tenant {tenant_id}. Created {records_created} records.")
        return True, f"Successfully processed {records_created} records"
        
    except Exception as e:
        error_msg = f"Unexpected error processing file {file_key}: {str(e)}"
        print(f"❌ {error_msg}")
        return False, error_msg
