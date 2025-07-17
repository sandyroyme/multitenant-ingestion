from django.db import models
class DataRecord(models.Model):
    tenant_id = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    device_id = models.CharField(max_length=100, blank=True, null=True)
    device_type = models.CharField(max_length=100, blank=True, null=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    approval_date = models.DateField(blank=True, null=True)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
