from django.urls import path

from .views import (
    Index,
    Index2,
    ListDeportista,
    DetailDeportista,
    CreateDeportista,
    UpdateDeportista,
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
]
