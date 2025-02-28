import requests
from django.core.files.storage import default_storage
def send_to_telegram(full_name, phone, description, file=None):
    bot_token = "7207281498:AAGY3cNi4wkNfgIFtRL2Gmp5K7bA2K_u5UI"  # Убедись, что токен корректен
    chat_id = "844551631"  # Убедись, что это правильный ID чата

    # Проверка токена
    if not bot_token:
        print("Ошибка: токен бота отсутствует или неверный.")
        return

    # Основное сообщение
    message = (
        f"Новая заявка на обратную связь:\n"
        f"ФИО: {full_name}\n"
        f"Телефон: {phone}\n"
        f"Описание: {description}\n"
    )

    # Отправка текстового сообщения
    url_message = f"https://api.telegram.org/bot7207281498:AAGY3cNi4wkNfgIFtRL2Gmp5K7bA2K_u5UI/sendMessage"
    response_message = requests.post(url_message, data={"chat_id": chat_id, "text": message})

    # Проверяем успешность отправки сообщения
    if response_message.status_code == 200:
        print("Текстовое сообщение успешно отправлено в Telegram.")
    else:
        print(f"Ошибка при отправке текстового сообщения: {response_message.text}")

    # Если есть файл, отправляем его
    if file:
        try:
            # Убедимся, что файл не пустой
            if file.size == 0:
                print("Ошибка: переданный файл пустой.")
                return

            # URL для отправки файла
            url_file = f"https://api.telegram.org/bot 7207281498:AAGY3cNi4wkNfgIFtRL2Gmp5K7bA2K_u5UI/sendDocument"

            # Читаем файл из объекта InMemoryUploadedFile
            file_data = {"document": (file.name, file.read())}
            response_file = requests.post(url_file, data={"chat_id": chat_id}, files=file_data)

            # Проверяем успешность отправки файла
            if response_file.status_code == 200:
                print("Файл успешно отправлен в Telegram.")
            else:
                print(f"Ошибка при отправке файла: {response_file.text}")

        except Exception as e:
            print(f"Ошибка при работе с файлом: {e}")

def send_to_telegram(full_name, phone, description, file_url=None):
    """
    Отправляет данные заявки в Telegram.
    Если есть URL файла, отправляет его как документ.
    """
    # Формируем текстовое сообщение
    message = (
        f"Новая заявка на обратную связь:\n"
        f"ФИО: {full_name}\n"
        f"Телефон: {phone}\n"
        f"Описание: {description}"
    )

    # Отправляем текстовое сообщение
    url_message = f"https://api.telegram.org/bot{"7207281498:AAGY3cNi4wkNfgIFtRL2Gmp5K7bA2K_u5UI"}/sendMessage"
    data_message = {"chat_id": 844551631, "text": message}
    response_message = requests.post(url_message, data=data_message)

    if response_message.status_code == 200:
        print("Сообщение успешно отправлено в Telegram.")
    else:
        print(f"Ошибка при отправке сообщения: {response_message.text}")

    # Если есть URL файла, отправляем его
    if file_url:
        # Скачиваем файл из медиасервера
        file_path = default_storage.path(file_url)
        with open(file_path, 'rb') as file_obj:
            send_file_to_telegram(file_obj)

def send_file_to_telegram(file):
    """
    Отправляет файл в Telegram.
    """
    url_file = f"https://api.telegram.org/bot{7207281498:AAGY3cNi4wkNfgIFtRL2Gmp5K7bA2K_u5UI}/sendDocument"
    files = {'document': file}  # Файл для отправки
    data = {"chat_id": 844551631}

    response_file = requests.post(url_file, data=data, files=files)

    if response_file.status_code == 200:
        print("Файл успешно отправлен в Telegram.")
    else:
        print(f"Ошибка при отправке файла: {response_file.text}")