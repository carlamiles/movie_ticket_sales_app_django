from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^checkout$',views.show_checkout),
    url(r'^dashboard$',views.show_dashboard),
    url(r'^process_checkout$',views.checkout),
    url(r'^select_movie$',views.select_movie),
]