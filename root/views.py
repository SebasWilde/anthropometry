from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.models import User
# from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Deportista, Deporte, Institucion, Medida
from .forms import (
    DeportistaForm,
    DeporteForm,
    CategoriaForm,
    InstitucionForm,
    MedidaForm,
)


class Index2(View):
    template_class = 'root/index2.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_class, {})


class Index(LoginRequiredMixin, View):
    template_class = 'root/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_class, {})


# TODO: Do query
# TODO: On change ordering submit
# TODO: DO pagination
class ListDeportista(LoginRequiredMixin, ListView):
    model = Deportista
    template_name = 'root/list_deportista.html'
    paginate_by = 10

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', 'apellidos')
        return ordering


# TODO:Do tab of extra info
# TODO: Display text field
class DetailDeportista(LoginRequiredMixin, DetailView):
    model = Deportista
    template_name = 'root/detail_deportista.html'

    def get_context_data(self, **kwargs):
        context = super(DetailDeportista, self).get_context_data(**kwargs)
        medidas = Medida.objects.filter(deportista__id=self.kwargs.get('pk'))\
            .order_by('-fecha_registro')
        context['medidas'] = medidas
        return context


# TODO: Not allow create deportista or institucion
# TODO: Add personal info
class CreateDeportista(LoginRequiredMixin, CreateView):
    model = Deportista
    form_class = DeportistaForm
    form_class_deporte = DeporteForm
    form_class_asociacion = InstitucionForm
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


# TODO: Update personal info
class UpdateDeportista(LoginRequiredMixin, UpdateView):
    model = Deportista
    form_class = DeportistaForm
    template_name = 'root/add_deportista.html'


# TODO: Create categories
class CreateDeporte(LoginRequiredMixin, CreateView):
    model = Deporte
    form_class = DeporteForm
    form_class_2 = CategoriaForm

    def get_success_url(self):
        next_url = self.request.POST.get('url', 'index')
        return reverse_lazy(next_url)


# TODO: DO pagination
class ListDeporte(LoginRequiredMixin, ListView):
    model = Deporte
    template_name = 'root/list_deporte.html'
    form_class_deporte = DeporteForm
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ListDeporte, self).get_context_data(**kwargs)
        if 'form_deporte' not in context:
            context['form_deporte'] = self.form_class_deporte
        context['url'] = 'list-deporte'
        return context

# TODO: Detail Deporte

# TODO: Update Deporte and categori¿y


class CreateInstitucion(LoginRequiredMixin, CreateView):
    model = Institucion
    form_class = InstitucionForm
    template_name = 'includes/add_institucion.html'


class UpdateInstitucion(LoginRequiredMixin, UpdateView):
    model = Institucion
    form_class = InstitucionForm
    template_name = 'includes/add_institucion.html'


class ListInstitucion(LoginRequiredMixin, ListView):
    template_name = 'root/list_institucion.html'
    form_class_asociacion = InstitucionForm

    def get_queryset(self):
        queryset = Institucion.objects.filter(user=self.request.user)
        for institucion in queryset:
            number_of_deportista = Deportista.objects.filter(
                institucion=institucion).count()
            institucion.number_of_deportista = number_of_deportista
        return queryset


class CreateMedida(LoginRequiredMixin, CreateView):
    model = Medida
    form_class = MedidaForm
    template_name = 'root/add_medida.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deportista_id = self.kwargs.get('deportista_pk', None)
        if deportista_id:
            deportista = Deportista.objects.get(pk=deportista_id)
            context['deportista'] = deportista
        return context


class UpdateMedida(LoginRequiredMixin, UpdateView):
    model = Medida
    form_class = MedidaForm
    template_name = 'root/add_medida.html'



