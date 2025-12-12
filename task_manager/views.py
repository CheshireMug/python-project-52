from django.views.generic import TemplateView
from django.http import HttpResponse


class IndexView(TemplateView):
    template_name = 'index.html'


def trigger_error(request):
    a = None
    a.hello()
    return HttpResponse("Hello, world. You're at the pollapp index.")
