from django.shortcuts import render

def dept(request):
	return render(request, 'organizations/dept.html')
