from django.urls import path
from .views import upload_file_view, view_data, api_get_records
urlpatterns = [path('upload/', upload_file_view, name='upload_file'),
    path('data/', view_data, name='view_data'),
    path('api/records/', api_get_records)]
