"""
File: messaging/urls.py
Author: Yusuf (Student 3)
Purpose: URL patterns for the messaging app.
Co-authors: None
"""

from django.urls import path
from . import views

app_name = 'messages'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('compose/', views.compose, name='compose'),
    path('drafts/', views.drafts, name='drafts'),
    path('sent/', views.sent, name='sent'),
    path('conversation/<int:user_id>/', views.conversation, name='conversation'),
    path('conversation/<int:user_id>/send/', views.send_in_thread, name='send_in_thread'),
    path('<int:message_id>/send/', views.send_draft, name='send_draft'),
    path('<int:message_id>/delete/', views.delete_message, name='delete_message'),
]
