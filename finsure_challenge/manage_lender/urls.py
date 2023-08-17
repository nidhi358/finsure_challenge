from django.urls import path
from . import views
from django.conf import settings

 
urlpatterns = [
    path('lender', views.LenderView.as_view()),
    path('lender/<int:id>', views.LenderView.as_view()),
    path('upload/', views.CsvUploader.as_view()),
    path('download/', views.CsvDownload.as_view()),
]