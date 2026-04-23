from django.urls import path
from .views import report_view, download_excel, download_pdf

urlpatterns = [
    path('', report_view, name='summary'),
    path('excel/', download_excel, name='download_excel'),
    path('pdf/', download_pdf, name='download_pdf'),
]