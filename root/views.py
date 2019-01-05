from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
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


class ListDeportista(LoginRequiredMixin, ListView):
    model = Deportista
    template_name = 'root/list_deportista.html'
    paginate_by = 10

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', 'apellidos')
        return ordering


class DetailDeportista(LoginRequiredMixin, DetailView):
    model = Deportista
    template_name = 'root/detail_deportista.html'


class CreateDeportista(CreateView):
    model = Deportista
    form_class = DeportistaForm
    template_name = 'root/add_deportista.html'


class UpdateDeportista(UpdateView):
    model = Deportista
    form_class = DeportistaForm
    template_name = 'root/add_deportista.html'
