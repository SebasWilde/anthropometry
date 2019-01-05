from django.views import View
from django.views.generic import CreateView, DetailView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Deportista
from .forms import DeportistaForm


class Index2(View):
    template_class = 'root/index2.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_class, {})


class Index(LoginRequiredMixin, View):
    template_class = 'root/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_class, {})


class DetailDeportista(LoginRequiredMixin, DetailView):
    model = Deportista
    template_name = 'root/detail_deportista.html'


class CreateDeportista(CreateView):
    model = Deportista
    form_class = DeportistaForm
    template_name = 'root/add_deportista.html'
