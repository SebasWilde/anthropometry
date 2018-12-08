from django.views import View
from django.shortcuts import render


class Index2(View):
    template_class = 'root/index2.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_class, {})


class Index(View):
    template_class = 'root/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_class, {})
