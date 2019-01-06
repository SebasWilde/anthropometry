from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Deportista, Deporte, Asociacion, Medida
from .forms import DeportistaForm, DeporteForm, AsociacionForm, MedidaForm


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

    def get_context_data(self, **kwargs):
        context = super(DetailDeportista, self).get_context_data(**kwargs)
        medidas = Medida.objects.filter(deportista__id=self.kwargs.get('pk'))\
            .order_by('fecha_registro')
        context['medidas'] = medidas
        return context


class CreateDeportista(LoginRequiredMixin, CreateView):
    model = Deportista
    form_class = DeportistaForm
    form_class_deporte = DeporteForm
    form_class_asociacion = AsociacionForm
    template_name = 'root/add_deportista.html'

    def get_context_data(self, **kwargs):
        context = super(CreateDeportista, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class
        if 'form_deporte' not in context:
            context['form_deporte'] = self.form_class_deporte
        if 'form_asociacion' not in context:
            context['form_asociacion'] = self.form_class_asociacion
        context['url'] = 'add-deportista'
        return context


class UpdateDeportista(LoginRequiredMixin, UpdateView):
    model = Deportista
    form_class = DeportistaForm
    template_name = 'root/add_deportista.html'


class CreateDeporte(LoginRequiredMixin, CreateView):
    model = Deporte
    form_class = DeporteForm

    def get_success_url(self):
        next_url = self.request.POST.get('url', 'index')
        return reverse_lazy(next_url)


class CreateAsociacion(LoginRequiredMixin, CreateView):
    model = Asociacion
    form_class = AsociacionForm

    def get_success_url(self):
        next_url = self.request.POST.get('url', 'index')
        return reverse_lazy(next_url)


class CreateMedida(LoginRequiredMixin, CreateView):
    model = Medida
    form_class = MedidaForm
    template_name = 'root/add_medida.html'


