# Multitenant Data Ingestion System

A robust, scalable data ingestion system built with Django that supports multitenant file processing using Kafka for asynchronous message handling and AWS S3 for file storage.

## 🏗️ Architecture Overview

This system implements an event-driven architecture with the following components:

- **Django Web Application**: Handles file uploads and provides REST APIs
- **Apache Kafka**: Message broker for asynchronous file processing
- **AWS S3 Cloud storage for uploaded files
- **PostgreSQL**: Database for storing processed data records
- **Kafka Consumer Service**: Background service for processing uploaded files

## 🚀 Features

- **Multitenant Support**: Isolated data processing per tenant
- **Asynchronous Processing**: Non-blocking file processing using Kafka
- **File Format Support**: CSV file processing (Excel files rejected gracefully)
- **Resilient Service**: Kafka consumer continues running despite errors
- **REST API**: JSON endpoints for data retrieval
- **Web Interface**: User-friendly file upload and data viewing interface
- **Automatic Topic Creation**: Kafka topics created automatically if missing
- **Comprehensive Error Handling**: Detailed error logging and failure events

## 🛠️ Technology Stack

### Backend Framework
- **Django 4.2+**: Web framework for building the application
- **Django REST Framework**: For building REST APIs
- **django-environ**: Environment variable management

### Message Queue & Streaming
- **Apache Kafka**: Distributed streaming platform
- **confluent-kafka**: Python client for Kafka
- **kafka-python**: Additional Kafka utilities for topic management

### Cloud Services
- **AWS S3**: Object storage for file uploads
- **boto3**: AWS SDK for Python

### Database
- **PostgreSQL**: Primary database

### Development Tools
- **Python 3.12 pogramming language
- **pip**: Package manager

## 📋 Prerequisites

Before setting up the project, ensure you have the following installed:

- Python 3.8 or higher
- Install AWS Cli and configure Credentials
- pip (Python package installer)
- Apache Kafka (local or remote instance)
- AWS S3 (for file storage)
- PostgreSQL (optional, SQLite used by default)

## 🔧 Installation & Setup

### 0. Download the ZIP

### 1. Unzip the source folder

```bash
cd multitenant_ingestion
```

###2irtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.psi
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root with the following variables:

```env
# Django Configuration
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Configuration (optional - SQLite used by default)
DATABASE_URL=postgresql://user:password@localhost:5432/db_name

AWS Configuration
AWS_STORAGE_BUCKET_NAME=your-s3-bucket-name

# Kafka Configuration
KAFKA_BROKER_URL=localhost:9092 (Depends on which kafka service to use)
KAFKA_TOPIC=file_uploaded
KAFKA_FAILURE_TOPIC=file_failed
```

# Create Database
create a new DB 
create user with password
grant access to the user on the DB
Once it is done update the DATABASE_URL in step 4
```
```bash
# Run database migrations
python manage.py migrate
```

### 6. Kafka Setup

Ensure Kafka is running on your system:

```bash
# Start Kafka (example with Docker)
Ensure Kafka service is available up and running
- Can be a local instance
   - Install Docker
   - Pull Kafka Image
   - Run Kafka (http://localhost:9092)
- Or any other remote service which can be consumebale

## 🚀 Running the Application

### 1. Start the Django Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:80000`

### 7. The Kafka Consumer Service

In a separate terminal: This is a custom Django command created 

```bash
python manage.py kafka_consumer
```

This starts the background service that processes uploaded files.

## 📊 Data Model

### DataRecord Model

The system stores processed data in the `DataRecord` model with the following fields:

- `tenant_id` (CharField): Unique identifier for the tenant
- `model` (CharField): Device model information
- `device_id` (CharField): Unique device identifier
- `device_type` (CharField): Type of device
- `manufacturer` (CharField): Device manufacturer
- `approval_date` (DateField): Device approval date
- `data` (JSONField): Complete row data as JSON - (reason of keeping this column is to be able to handle any new properties in the csv file)
- `created_at` (DateTimeField): Record creation timestamp

## 🔌 API Endpoints

### REST API

#### GET `/api/records/`
Retrieve data records with optional filtering.

**Query Parameters:**
- `tenant_id` (optional): Filter by tenant ID
- `device_id` (optional): Filter by device ID

**Example:**
http://127.0.0.1:8000/api/records/?tenant_id=mmmm&device_id=201

**Response:**
```json
[
    {
        "id": 9,
        "tenant_id": "mmmm",
        "model": "GE-MRI-1000",
        "device_id": "201",
        "device_type": null,
        "manufacturer": "General Electric",
        "approval_date": null,
        "data": {
            "Model": "GE-MRI-1000",
            "Device_id": "201",
            "Tenant_id": "Manipal_01",
            "Device_Type": "MRI Scanner",
            "Manufacturer": "General Electric",
            "Approval_Date": "2022-01-20"
        },
        "created_at": "2025-07-16T20:15:42.793767Z"
    }
]
```

## 🔌 Web Interface

#### GET `/upload/`
File upload interface with form-based upload.

#### GET `/data/`
http://127.0.0.1:8000/data/
Data viewing interface with filtering options.

## 🔒 Security Analysis

### Authentication & Authorization

**Current Status: ❌ No Authentication Implemented**

The application currently has **NO authentication or authorization** mechanisms (because it's just a POC):

- All endpoints are publicly accessible
- No user authentication applied
- No role-based access control implemented
- No API key validation not in place
- No session management for file uploads

### Current Security Vulnerabilities

1. **Public API Access**: All endpoints are publicly accessible
2. **No Input Validation**: Limited validation on file uploads
3. **No Rate Limiting**: No protection against abuse
4. **Debug Mode**: DEBUG=true

## 📁 Project Structure

```
multitenant_ingestion/
├── ingestion/                    # Main Django app
│   ├── management/
│   │   └── commands/
│   │       └── kafka_consumer.py # Kafka consumer service
│   ├── migrations/               # Database migrations
│   ├── templates/                # HTML templates
│   │   ├── upload.html          # File upload interface
│   │   └── data_list.html       # Data viewing interface
│   ├── business_logic.py        # File processing logic
│   ├── forms.py                 # Django forms
│   ├── models.py                # Database models
│   ├── serializers.py           # DRF serializers
│   ├── s3_utils.py              # AWS S3 utilities
│   ├── tasks.py                 # Kafka event handling
│   ├── urls.py                  # URL routing
│   └── views.py                 # View logic
├── multitenant_ingestion/        # Django project settings
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Main URL configuration
│   └── wsgi.py                  # WSGI configuration
├── kafka_consumer.py            # Standalone Kafka consumer (legacy)
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🔄 Data Flow. **File Upload**: User uploads CSV file via web interface
2. **S3 Storage**: File is uploaded to AWS S3 with tenant-specific path
3. **Kafka Event**: File upload event is sent to Kafka topic
4. **Background Processing**: Kafka consumer processes the file asynchronously
5. **Data Extraction**: CSV data is parsed and validated
6. **Database Storage**: Records are created in the database
7. **Cleanup**: Original file is deleted from S3
8. **Error Handling**: Failures are logged and sent to failure topic

## 🐛 Troubleshooting

### Common Issues

1. **Kafka Connection Error**
   - Ensure Kafka is running on the configured broker URL
   - Check network connectivity
   - Verify topic exists or auto-creation is enabled

2. **S3 Upload Failures**
   - Verify AWS credentials are configured
   - Check S3 bucket permissions
   - Ensure bucket exists

3. **Database Connection Issues**
   - Verify database is running
   - Check connection string in environment variables
   - Run migrations if needed

4. **File Processing Errors**
   - Ensure files are in CSV format
   - Check file encoding (UTF-8 recommended)
   - Verify required columns exist

### Logs and Debugging

- Django logs: Check console output during development
- Kafka consumer logs: Monitor the consumer service output
- Database logs: Check database server logs
- S3 logs: Monitor AWS CloudTrail for S3 access
```
