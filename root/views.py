from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.models import User
# from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Deportista, Deporte, Institucion, Medida, Categoria
from .forms import (
    DeportistaForm,
    DeporteForm,
    CategoriaForm,
    InstitucionForm,
    MedidaForm,
    DeportistaInfoForm,
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
        medidas = Medida.objects.filter(deportista__id=self.kwargs.get('pk')) \
            .order_by('-fecha_registro')
        context['medidas'] = medidas
        return context


# TODO: Add personal info
class CreateDeportista(LoginRequiredMixin, CreateView):
    model = Deportista
    form_class = DeportistaForm
    DeportistaInfoForm = DeportistaInfoForm
    template_name = 'root/add_deportista.html'

    def get_context_data(self, **kwargs):
        context = super(CreateDeportista, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class
        if 'form_info' not in context:
            context['form_info'] = self.DeportistaInfoForm
        context['url'] = 'add-deportista'
        return context


# TODO: Update personal info
class UpdateDeportista(LoginRequiredMixin, UpdateView):
    model = Deportista
    form_class = DeportistaForm
    template_name = 'root/add_deportista.html'


class CreateDeporte(LoginRequiredMixin, CreateView):
    model = Deporte
    form_class = DeporteForm
    template_name = 'includes/add_deporte.html'


class UpdateDeporte(LoginRequiredMixin, UpdateView):
    model = Deporte
    form_class = DeporteForm
    template_name = 'includes/add_deporte.html'


# TODO: DO pagination
class ListDeporte(LoginRequiredMixin, ListView):
    model = Deporte
    template_name = 'root/list_deporte.html'

    def get_queryset(self):
        queryset = Deporte.objects.all()
        for deporte in queryset:
            number_of_deportista = Deportista.objects.filter(
                deporte=deporte).count()
            deporte.number_of_deportista = number_of_deportista
        return queryset


# TODO: Add pagination to categories
class DetailDeporte(LoginRequiredMixin, DetailView):
    model = Deporte
    template_name = 'root/detail_deporte.html'

    def get_object(self, queryset=None):
        object = super(DetailDeporte, self).get_object(queryset)
        number_of_deportista = Deportista.objects.filter(
            deporte=object).count()
        object.number_of_deportista = number_of_deportista
        return object

    def get_context_data(self, **kwargs):
        context = super(DetailDeporte, self).get_context_data(**kwargs)
        categorias = Categoria.objects.filter(deporte__id=self.kwargs.get('pk'))
        for categoria in categorias:
            number_of_deportista = Deportista.objects.filter(
                categoria=categoria).count()
            categoria.number_of_deportista = number_of_deportista
        context['categorias'] = categorias
        return context


class CreateCategoria(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'includes/add_categoria.html'


class UpdateCategoria(LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'includes/add_categoria.html'


class CreateInstitucion(LoginRequiredMixin, CreateView):
    model = Institucion
    form_class = InstitucionForm
    template_name = 'includes/add_institucion.html'


class UpdateInstitucion(LoginRequiredMixin, UpdateView):
    model = Institucion
    form_class = InstitucionForm
    template_name = 'includes/add_institucion.html'


# TODO: DO pagination
class ListInstitucion(LoginRequiredMixin, ListView):
    template_name = 'root/list_institucion.html'

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



