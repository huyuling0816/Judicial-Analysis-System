from django.shortcuts import render,HttpResponse

# Create your views here.


def fun(request):
    return render(request, 'htmlfile.html')