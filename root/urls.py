from django.urls import path

from .views import (
    Index,
    Index2,
    DetailDeportista,
    CreateDeportista,
)


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('2/', Index2.as_view(), name='index2'),
    path('deportista/detail/<int:pk>', DetailDeportista.as_view(),
         name='detail-deportista'),
    path('deportista/add/', CreateDeportista.as_view(), name='add-deportista'),
]
