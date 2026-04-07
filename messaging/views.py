from django.shortcuts import render

# Create your views here.
def inbox(request):
    return render(request, 'messaging/inbox.html')