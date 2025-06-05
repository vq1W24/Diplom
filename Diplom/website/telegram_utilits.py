import requests
from django.core.files.storage import default_storage


def send_to_telegram(full_name, phone, description, file=None):
    """
    Отправляет данные заявки в Telegram.
    При наличии файла — отправляет его как документ.
    """
    from django.conf import settings  # импорт внутри функции, чтобы избежать циклической зависимости

    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID

    message = (
        f"Новая заявка на обратную связь:\n"
        f"ФИО: {full_name}\n"
        f"Телефон: {phone}\n"
        f"Описание: {description}"
    )

    # Отправляем текстовое сообщение
    url_message = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data_message = {"chat_id": chat_id, "text": message}

    response_message = requests.post(url_message, data=data_message)

    if response_message.status_code == 200:
        print("Сообщение успешно отправлено в Telegram.")
    else:
        print(f"Ошибка при отправке сообщения: {response_message.text}")

    if file:
        try:
            if file.size == 0:
                print("Ошибка: переданный файл пустой.")
                return

            url_file = f"https://api.telegram.org/bot{bot_token}/sendDocument"
            file_data = {"document": (file.name, file.read())}
            response_file = requests.post(url_file, data={"chat_id": chat_id}, files=file_data)

            if response_file.status_code == 200:
                print("Файл успешно отправлен в Telegram.")
            else:
                print(f"Ошибка при отправке файла: {response_file.text}")

        except Exception as e:
            print(f"Ошибка при работе с файлом: {e}")