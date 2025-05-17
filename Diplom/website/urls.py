from django.urls import path
from . import views
from .forms import ContactRequestDeleteView
from .views import ContactRequestListView, UpdateStatus, ContactRequestDetailView, CreateContactRequest,ContactRequestEditView

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.service, name='services'),
    path('about/', views.about, name='about'),
    path('news/', views.news, name='news'),
    path('contact/', views.contact, name='contact'),
    # path('login/', views.login, name='login'),
    path('list/', ContactRequestListView.as_view(), name='contact_request_list'),  # Имя маршрута 'contact_request_list'
    path('update/<int:pk>/', UpdateStatus.as_view(), name='contact_request_update'),  # Имя маршрута 'contact_request_update'
    path('create/', CreateContactRequest.as_view(), name='contact_request_create'),  # Новый маршрут для создания заявки
    path('detail/<int:pk>/', ContactRequestDetailView.as_view(), name='contact_request_detail'),
    path('delete/<int:pk>/', ContactRequestDeleteView.as_view(), name='contact_request_delete'),      # Удаление заявки

    path('edit/<int:pk>/', ContactRequestEditView.as_view(), name='contact_request_edit'),     # Редактирование заявки


]
