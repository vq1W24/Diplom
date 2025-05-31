from django.urls import path

from .forms import ContactRequestDeleteView
from .views import index, service, about, news, contact,applications_list, update_status_ajax

from .views import ContactRequestListView, UpdateStatus, CreateContactRequest, ContactRequestDetailView,  ContactRequestEditView
from django.conf import settings
from django.conf.urls.static import static
from .views import LoginUser

from django.contrib.auth import views as auth_views

urlpatterns = [
    # Главная страница
    path('', index, name='index'),
    
    # Страницы сайта
    path('services/', service, name='services'),
    path('about/', about, name='about'),
    path('news/', news, name='news'),
    path('contact/', contact, name='contact'),

    # Заявки
    path('list/', ContactRequestListView.as_view(), name='contact_request_list'),
    path('update/<int:pk>/', UpdateStatus.as_view(), name='contact_request_update'),
    path('create/', CreateContactRequest.as_view(), name='contact_request_create'),
    path('detail/<int:pk>/', ContactRequestDetailView.as_view(), name='contact_request_detail'),
    path('delete/<int:pk>/', ContactRequestDeleteView.as_view(), name='contact_request_delete'),
    path('edit/<int:pk>/', ContactRequestEditView.as_view(), name='contact_request_edit'),
    path('applications/', applications_list, name='applications'),
    path('update-status-ajax/', update_status_ajax, name='update_status_ajax'),

    # Авторизация
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)