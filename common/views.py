from django.shortcuts import render


def error400(request):
    return render(request, 'errors/error-400.html')

def error403(request):
    return render(request, 'errors/error-403.html')

def error404(request):
    return render(request, 'errors/error-404.html')

def error500(request):
    return render(request, 'errors/error-500.html')
