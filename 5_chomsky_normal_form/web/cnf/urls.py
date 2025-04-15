from django.urls import path
from . import views

urlpatterns = [
    # path('', views.form_view, name='form'),
    # path('success/', views.success_view, name='success'),
    path('', views.grammar_view, name="grammar_input"),
]
