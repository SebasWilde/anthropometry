from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Deportista, Deporte, Institucion, Medida, Categoria, DeportistaInfo
from .forms import (
    DeportistaForm,
    DeporteForm,
    CategoriaForm,
    InstitucionForm,
    MedidaForm,
    DeportistaInfoForm,
)


class Index(LoginRequiredMixin, View):
    template_class = 'root/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_class, {})


class ListDeportista(LoginRequiredMixin, ListView):
    model = Deportista
    template_name = 'root/list_deportista.html'
    paginate_by = 10

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        if search:
            queryset = Deportista.objects.filter(
                Q(nombres__icontains=search) | Q(apellidos__icontains=search))
        else:
            queryset = Deportista.objects.all()
        return queryset.order_by('apellidos', 'nombres')

    def get_context_data(self, **kwargs):
        context = super(ListDeportista, self).get_context_data(**kwargs)
        search = self.request.GET.get('search', None)
        if search:
            context['search'] = search
        return context


class DetailDeportista(LoginRequiredMixin, DetailView):
    model = Deportista
    template_name = 'root/detail_deportista.html'

    def get_context_data(self, **kwargs):
        context = super(DetailDeportista, self).get_context_data(**kwargs)
        medidas_list = Medida.objects.filter(deportista__id=self.kwargs.get('pk')) \
            .order_by('-fecha_registro')
        paginator = Paginator(medidas_list, 10)
        page = self.request.GET.get('page')
        medidas = paginator.get_page(page)
        context['medidas'] = medidas
        context['is_paginated'] = paginator.num_pages > 1
        return context


class CreateDeportista(LoginRequiredMixin, CreateView):
    model = Deportista
    form_class = DeportistaForm
    second_form_class = DeportistaInfoForm
    template_name = 'root/add_deportista.html'

    def get_context_data(self, **kwargs):
        context = super(CreateDeportista, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class
        if 'form_info' not in context:
            context['form_info'] = self.second_form_class
        context['url'] = 'add-deportista'
        return context

    def post(self, request, *args, **kwargs):
        form_deportista = self.form_class(request.POST)
        form_info_deportista = self.second_form_class(request.POST)
        if form_deportista.is_valid() and form_info_deportista.is_valid():
            deportista = form_deportista.save()
            info_deportista = form_info_deportista.save(commit=False)
            info_deportista.deportista = deportista
            info_deportista.save()

            return HttpResponseRedirect(deportista.get_absolute_url())
        else:
            return self.render_to_response(self.get_context_data(
                form=form_deportista, form_info=form_info_deportista))


class UpdateDeportista(LoginRequiredMixin, UpdateView):
    model = Deportista
    second_model = DeportistaInfo
    form_class = DeportistaForm
    second_form_class = DeportistaInfoForm
    template_name = 'root/add_deportista.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateDeportista, self).get_context_data(**kwargs)

        if 'form' not in context:
            context['form'] = self.form_class
        if 'form_info' not in context:
            context['form_info'] = self.second_form_class
        context['url'] = 'add-deportista'
        return context

    def post(self, request, *args, **kwargs):
        deportista = Deportista.objects.get(pk=kwargs['pk'])
        try:
            info_deportista = DeportistaInfo.objects.get(deportista=deportista)
        except DeportistaInfo.DoesNotExist:
            info_deportista = DeportistaInfo.objects.create(deportista=deportista)
        form_deportista = self.form_class(request.POST, instance=deportista)
        form_info_deportista = self.second_form_class(
            request.POST, instance=info_deportista)
        if form_deportista.is_valid() and form_info_deportista.is_valid():
            form_deportista.save()
            form_info_deportista.save()

            return HttpResponseRedirect(deportista.get_absolute_url())
        else:
            return self.render_to_response(self.get_context_data(
                form=form_deportista, form_info=form_info_deportista))


class CreateDeporte(LoginRequiredMixin, CreateView):
    model = Deporte
    form_class = DeporteForm
    template_name = 'includes/add_deporte.html'


class UpdateDeporte(LoginRequiredMixin, UpdateView):
    model = Deporte
    form_class = DeporteForm
    template_name = 'includes/add_deporte.html'


class ListDeporte(LoginRequiredMixin, ListView):
    model = Deporte
    template_name = 'root/list_deporte.html'
    paginate_by = 10

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        if search:
            queryset = Deporte.objects.filter(deporte__icontains=search)
        else:
            queryset = Deporte.objects.all()
        queryset = queryset.annotate(number_of_deportista=Count('deportista'))
        return queryset.order_by('deporte')

    def get_context_data(self, **kwargs):
        context = super(ListDeporte, self).get_context_data(**kwargs)
        search = self.request.GET.get('search', None)
        if search:
            context['search'] = search
        return context


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
        categorias_list = Categoria.objects.filter(deporte__id=self.kwargs.get('pk'))
        for categoria in categorias_list:
            number_of_deportista = Deportista.objects.filter(
                categoria=categoria).count()
            categoria.number_of_deportista = number_of_deportista
        paginator = Paginator(categorias_list, 10)
        page = self.request.GET.get('page')
        categorias = paginator.get_page(page)
        context['is_paginated'] = paginator.num_pages > 1
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


class ListInstitucion(LoginRequiredMixin, ListView):
    template_name = 'root/list_institucion.html'
    paginate_by = 10

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        if search:
            queryset = Institucion.objects.filter(user=self.request.user,
                                                  nombre__icontains=search)
        else:
            queryset = Institucion.objects.filter(user=self.request.user)
        queryset = queryset.annotate(number_of_deportista=Count('deportista'))
        return queryset.order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super(ListInstitucion, self).get_context_data(**kwargs)
        search = self.request.GET.get('search', None)
        if search:
            context['search'] = search
        return context


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


class ReporterView(LoginRequiredMixin, View):
    template_name = 'root/reportes.html'

    def get(self, request, *args, **kwargs):
        reporter_type = request.GET.get('reporter_type', 'entrenador')
        context = dict()
        instituciones = Institucion.objects.filter(user=request.user)
        if reporter_type == 'entrenador':
            deportes = Deporte.objects.all()
            categorias = Categoria.objects.all()
            context = {
                'deportes': deportes,
                'categorias': categorias,
            }
        elif reporter_type == 'deportista':
            deportistas = Deportista.objects.all()
            context = {
                'deportistas': deportistas,
            }
        context['reporter_type'] = reporter_type
        context['instituciones'] = instituciones
        return render(request, self.template_name, context)


class ReporterTrainerView(LoginRequiredMixin, View):
    template_name = 'root/reportes_entrenador.html'

    def get(self, request, *args, **kwargs):
        deporte = request.GET.get('deporte', None)
        date_input = request.GET.get('date', None)
        institucion = request.GET.get('institucion', None)
        if not deporte and not institucion:
            return HttpResponseRedirect(reverse_lazy('reporter'))
        categoria = request.GET.get('categoria', None)
        if categoria:
            deportistas = Deportista.objects.filter(deporte=deporte,
                                                    categoria=categoria,
                                                    institucion=institucion)
        else:
            deportistas = Deportista.objects.filter(deporte=deporte,
                                                    institucion=institucion)

        if date_input:
            year, month = date_input.split('-')
            mediciones = Medida.objects.filter(
                deportista__in=deportistas,
                fecha_registro__month__gte=month,
                fecha_registro__year__gte=year
            ).order_by('-fecha_registro')
        else:
            mediciones = Medida.objects.filter(deportista__in=deportistas) \
                .order_by('-fecha_registro')
        input_get = {
            'deporte': deporte,
            'date': date_input,
            'categoria': categoria,
            'institucion': institucion,
        }
        context = {
            'mediciones': mediciones,
            'input_get': input_get,
        }

        return render(request, self.template_name, context)


class ReporterDeportistaView(LoginRequiredMixin, View):
    template_name = 'root/reportes_deportista.html'

    def get(self, request, *args, **kwargs):
        deportista_pk = request.GET.get('deportista', None)
        date_input = request.GET.get('date', None)
        if not deportista_pk:
            return HttpResponseRedirect(reverse_lazy('reporter'))
        deportista = Deportista.objects.get(pk=deportista_pk)
        if date_input:
            year, month = date_input.split('-')
            mediciones = Medida.objects.filter(
                deportista=deportista,
                fecha_registro__month__gte=month,
                fecha_registro__year__gte=year
            ).order_by('fecha_registro')
        else:
            mediciones = Medida.objects.filter(deportista=deportista) \
                .order_by('fecha_registro')
        context = {
            'mediciones': mediciones,
            'deportista': deportista,
            'input_get': request.GET,
        }

        return render(request, self.template_name, context)
