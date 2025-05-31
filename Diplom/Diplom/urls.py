"""
URL configuration for Diplom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView

from website import views
from website.forms import ContactRequestDeleteView
from website.views import ContactRequestListView, UpdateStatus, CreateContactRequest, ContactRequestDetailView, \
    ContactRequestEditView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),  # Замените myapp на имя вашего приложения

    path('', views.index, name='index'),
    path('services/', views.service, name='services'),
    path('about/', views.about, name='about'),
    path('news/', views.news, name='news'),
    path('contact/', views.contact, name='contact'),
    path('list/', ContactRequestListView.as_view(), name='contact_request_list'),  # Имя маршрута 'contact_request_list'
    path('update/<int:pk>/', UpdateStatus.as_view(), name='contact_request_update'),
    path('create/', CreateContactRequest.as_view(), name='contact_request_create'),  # Новый маршрут для создания заявки
    path('detail/<int:pk>/', ContactRequestDetailView.as_view(), name='contact_request_detail'),
    path('delete/<int:pk>/', ContactRequestDeleteView.as_view(), name='contact_request_delete'),
    path('edit/<int:pk>/', ContactRequestEditView.as_view(), name='contact_request_edit'),  # Редактирование заявки
    path('privacy-policy/', TemplateView.as_view(template_name='privacy-policy.html'), name='privacy_policy'),

    path('accounts/', include('django.contrib.auth.urls')),

]


