from django.http import HttpResponse


def home(request):
    return HttpResponse('<html><body>Olá Mundo</body></html>')
