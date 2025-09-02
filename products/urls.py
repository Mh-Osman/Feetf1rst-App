from django.urls import path
from . import views

urlpatterns = [
    path("shoes/", views.shoe_list, name="shoe-list"),          # GET all
    path("create/", views.shoe_create, name="shoe-create"),  # POST shoe
    path("shoes/<int:pk>/", views.shoe_detail, name="shoe-detail"),  # GET one, PUT, PATCH
]
