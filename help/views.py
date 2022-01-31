from django.shortcuts import render

# Create your views here.
def helpList(request):
    return render(request, 'base/help.html', {})