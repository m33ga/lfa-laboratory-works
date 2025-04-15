from django.urls import path
from . import views

urlpatterns = [
    path('', views.grammar_view, name="grammar_input"),
]
