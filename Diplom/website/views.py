from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.urls import reverse_lazy
import datetime
from django.shortcuts import render, get_object_or_404, redirect
import feedparser
from django.shortcuts import render
from .models import FNSNews
from datetime import datetime
from django.utils.timezone import make_aware
from .forms import ContactForm, StatusUpdateForm, CreateRequestForm, ContactRequestForm
from django.core.files.storage import FileSystemStorage
from django.utils import timezone  # Используйте timezone из Django
from .models import ContactRequest
from .telegram_utilits import send_to_telegram  # Импорт функции для Telegram
from django.views.generic import ListView, UpdateView, DetailView, CreateView


def index(request):
        return render(request, 'index.html')

def service(request):
    return render(request, 'service.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact_request = form.save()
            if request.method == 'POST':
                form = ContactForm(request.POST, request.FILES)
                if form.is_valid():
                    # Проверяем наличие согласия
                    if not request.POST.get('pd_agreement'):
                        return render(request, 'contact.html', {
                            'form': form,
                            'error': 'Необходимо дать согласие на обработку персональных данных'
                        })

                    contact_request = form.save(commit=False)
                    contact_request.pd_agreement = True  # Сохраняем факт согласия
                    contact_request.pd_agreement_date = timezone.now()  # Дата согласия
                    contact_request.save()


            # Обрабатываем файл, если он есть
            file  = None
            if 'file' in request.FILES:
                uploaded_file = request.FILES['file']
                fs = FileSystemStorage()
                filename = fs.save(uploaded_file.name, uploaded_file)
                file_url = fs.url(filename)

            # Отправляем данные в Telegram
            send_to_telegram(
                full_name=contact_request.full_name,
                phone=contact_request.phone,
                description=contact_request.description,
                # file=request.FILES.get('file')
            )

            return render(request, 'contact_success.html')

    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def list(request):
    return render(request, 'list.html')


def news (request):
    news_list = []  # Инициализируем пустой список

    try:
        # Парсинг RSS ленты ФНС
        feed = feedparser.parse("https://www.nalog.gov.ru/rss/")

        # Очищаем старые новости и сохраняем новые
        FNSNews.objects.all().delete()

        for entry in feed.entries:
            try:
                published = make_aware(datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z'))
                FNSNews.objects.create(
                    title=entry.title,
                    summary=entry.summary,
                    link=entry.link,
                    published=published
                )
            except (KeyError, ValueError) as e:
                print(f"Ошибка обработки новости: {e}")
                continue

        # Получаем все новости из БД
        news_list = FNSNews.objects.all().order_by('-published')

    except Exception as e:
        print(f"Ошибка при получении новостей: {e}")
        # Можно добавить сообщение об ошибке для пользователя
        news_list = FNSNews.objects.all().order_by('-published') if FNSNews.objects.exists() else []

    return render(request, 'news.html', {'      news_list': news_list})

class ContactRequestListView(ListView):
    model = ContactRequest
    template_name = 'list.html'  # Имя вашего шаблона
    context_object_name = 'contact_requests'
    paginate_by = 10  # Пагинация по 10 заявок на странице

    def get_queryset(self):
        queryset = super().get_queryset()

        # Поиск
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(full_name__icontains=search_query) |
                Q(phone__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(request_number__icontains=search_query)
            )

        # Фильтрация по дате
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if date_from:
            date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d').date()
            queryset = queryset.filter(created_at__date__gte=date_from)

        if date_to:
            date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d').date()
            queryset = queryset.filter(created_at__date__lte=date_to)

        return queryset

    def post(self, request, *args, **kwargs):
        # Обработка POST-запроса для изменения статуса
        contact_request_id = request.POST.get('contact_request_id')
        new_status = request.POST.get('status')

        if contact_request_id and new_status:
            contact_request = get_object_or_404(ContactRequest, pk=contact_request_id)

            # Создаем экземпляр формы с данными из POST-запроса
            form = StatusUpdateForm(request.POST, instance=contact_request)
            if form.is_valid():
                form.save()  # Сохраняем изменения
            else:
                print(form.errors)  # Выводим ошибки формы для отладки

        return redirect('contact_request_list')  # Перенаправляем обратно к списку заявок

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Передаем параметры поиска и фильтрации в контекст
        context['search'] = self.request.GET.get('search', '')
        context['date_from'] = self.request.GET.get('date_from', '')
        context['date_to'] = self.request.GET.get('date_to', '')

        # Передаем возможные значения статуса в контекст
        context['status_choices'] = ContactRequest.STATUS_CHOICES

        return context
class ContactRequestDetailView(DetailView):
    model = ContactRequest
    template_name = 'detail.html'  # Имя вашего шаблона
    context_object_name = 'contact_request'

class UpdateStatus(UpdateView):
    model = ContactRequest
    fields = ['status']
    template_name = 'update_status.html'  # Используйте отдельный шаблон для обновления статуса
    success_url = reverse_lazy('contact_request_list')  # Перенаправление после успешного обновления

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обновление статуса заявки'
        return context


class CreateContactRequest(CreateView):
    model = ContactRequest
    form_class = CreateRequestForm  # Используйте форму для создания заявки
    template_name = 'create_contact_request.html'
    success_url = reverse_lazy('contact_request_list')  # Перенаправление после успешного создания

class ContactRequestEditView(UpdateView):
    model = ContactRequest
    form_class = ContactRequestForm  # Форма для редактирования всех полей заявки
    template_name = 'edit_contact_request.html'  # Шаблон для редактирования заявки
    success_url = reverse_lazy('contact_request_list')  # Перенаправление после успешного сохранения
    context_object_name = 'contact_request'  # Имя объекта в контексте

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    extra_context = {'title': "Авторизация"}

class ContactRequestCreateView(CreateView):
    model = ContactRequest
    form_class = CreateRequestForm
    template_name = 'create_contact_request.html'
    success_url = reverse_lazy('contact_request_list')

    def form_valid(self, form):
        # Сохраняем форму
        response = super().form_valid(form)

        # Получаем данные из формы
        full_name = form.instance.full_name
        phone = form.instance.phone
        description = form.instance.description
        file = self.request.FILES.get('file')  # Получаем загруженный файл

        # Отправляем данные в Telegram
        send_to_telegram(full_name, phone, description, file)

        return response