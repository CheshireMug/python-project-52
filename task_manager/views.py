from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 1/0 # 'index.html'
