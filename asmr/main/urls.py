from django.urls import path
from . import views

urlpatterns = [
    path('import-audio/', views.AudioImportView.as_view(), name='audio-import'),
]