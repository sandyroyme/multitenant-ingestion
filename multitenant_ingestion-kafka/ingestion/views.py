from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DataRecord
from .forms import UploadFileForm
from .serializers import DataRecordSerializer
from .s3_utils import upload_file_to_s3
from .tasks import send_file_uploaded_event
def upload_file_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            tenant_id = form.cleaned_data['tenant_id']
            file = form.cleaned_data['file']
            key = upload_file_to_s3(file, tenant_id, file.name)
            send_file_uploaded_event(tenant_id, key)
            # Only allow CSV files
            if not file.name.endswith('.csv'):
                form.add_error('file', 'Only CSV files are allowed')
                return render(request, 'upload.html', {
                    'form': form,
                    'error': 'Please upload a CSV file only'
                })
            
            # Return to same page with success message
            return render(request, 'upload.html', {
                'form': UploadFileForm(),
                'success': f'File {file.name} uploaded successfully and queued for processing'
            })
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
def view_data(request):
    tenant_id = request.GET.get('tenant_id')
    device_id = request.GET.get('device_id')
    qs = DataRecord.objects.all()
    if tenant_id: qs = qs.filter(tenant_id=tenant_id)
    if device_id: qs = qs.filter(device_id=device_id)
    return render(request, 'data_list.html', {'records': qs})
@api_view(['GET'])
def api_get_records(request):
    tenant_id = request.GET.get('tenant_id')
    device_id = request.GET.get('device_id')
    if not tenant_id or not device_id:
        return Response({
            "error": "Both tenant_id and device_id parameters are required"
        }, status=400)
    qs = DataRecord.objects.all()
    if tenant_id: qs = qs.filter(tenant_id=tenant_id)
    if device_id: qs = qs.filter(device_id=device_id)
    return Response(DataRecordSerializer(qs, many=True).data)
