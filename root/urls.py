from django.urls import path

from .views import (
    Index,
    Index2,
    ListDeportista,
    DetailDeportista,
    CreateDeportista,
    UpdateDeportista,
    CreateDeporte,
    ListDeporte,
    CreateInstitucion,
    ListAsociacion,
    CreateMedida,
    UpdateMedida,
)


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('2/', Index2.as_view(), name='index2'),
    path('deportista/list/', ListDeportista.as_view(), name='list-deportista'),
    path('deportista/detail/<int:pk>/', DetailDeportista.as_view(),
         name='detail-deportista'),
    path('deportista/add/', CreateDeportista.as_view(), name='add-deportista'),
    path('deportista/edit/<int:pk>/', UpdateDeportista.as_view(),
         name='edit-deportista'),
    path('deporte/add/', CreateDeporte.as_view(), name='add-deporte'),
    path('deporte/list/', ListDeporte.as_view(), name='list-deporte'),
    path('asociacion/add/', CreateInstitucion.as_view(), name='add-asociacion'),
    path('asociacion/list/', ListAsociacion.as_view(), name='list-asociacion'),
    path('medida/add/', CreateMedida.as_view(), name='add-medida'),
    path('medida/add/<int:deportista_pk>/', CreateMedida.as_view(),
         name='add-medida'),
    path('medida/edit/<int:pk>/', UpdateMedida.as_view(), name='edit-medida'),
]
