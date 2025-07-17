from django import forms
class UploadFileForm(forms.Form):
    tenant_id = forms.CharField(max_length=100)
    file = forms.FileField()
