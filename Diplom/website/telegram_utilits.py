import requests
from django.core.files.storage import default_storage

# Константы для Telegram API
BOT_TOKEN = "7207281498:AAGY3cNi4wkNfgIFtRL2Gmp5K7bA2K_u5UI"
CHAT_ID = "844551631"

def send_to_telegram(full_name, phone, description, file=None):
    """
    Отправляет данные заявки в Telegram с возможностью прикрепления файла.
    
    Args:
        full_name (str): ФИО клиента
        phone (str): Телефон клиента
        description (str): Описание заявки
        file (File, optional): Файл для отправки. Defaults to None.
    
    Returns:
        bool: True если отправка успешна, False при ошибке
    """
    # Проверка токена
    if not BOT_TOKEN:
        print("Ошибка: токен бота отсутствует или неверный.")
        return False

    # Формирование сообщения
    message = (
        f"Новая заявка на обратную связь:\n"
        f"ФИО: {full_name}\n"
        f"Телефон: {phone}\n"
        f"Описание: {description}"
    )

    # Отправка текстового сообщения
    text_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        text_response = requests.post(
            text_url,
            data={"chat_id": CHAT_ID, "text": message},
            timeout=10
        )
        
        if text_response.status_code != 200:
            print(f"Ошибка при отправке сообщения: {text_response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения: {e}")
        return False

    # Отправка файла, если он есть
    if file:
        try:
            # Проверка размера файла
            if file.size == 0:
                print("Ошибка: переданный файл пустой.")
                return False

            # Подготовка файла
            file_data = {"document": (file.name, file.read())}
            file_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
            
            file_response = requests.post(
                file_url,
                data={"chat_id": CHAT_ID},
                files=file_data,
                timeout=30
            )

            if file_response.status_code != 200:
                print(f"Ошибка при отправке файла: {file_response.text}")
                return False
                
        except Exception as e:
            print(f"Ошибка при работе с файлом: {e}")
            return False

    return True


def send_file_from_url_to_telegram(full_name, phone, description, file_url=None):
    """
    Отправляет данные заявки в Telegram с файлом по URL.
    
    Args:
        full_name (str): ФИО клиента
        phone (str): Телефон клиента
        description (str): Описание заявки
        file_url (str, optional): URL файла. Defaults to None.
    
    Returns:
        bool: True если отправка успешна, False при ошибке
    """
    # Формирование сообщения
    message = (
        f"Новая заявка на обратную связь:\n"
        f"ФИО: {full_name}\n"
        f"Телефон: {phone}\n"
        f"Описание: {description}"
    )

    # Отправка текстового сообщения
    text_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        text_response = requests.post(
            text_url,
            data={"chat_id": CHAT_ID, "text": message},
            timeout=10
        )
        
        if text_response.status_code != 200:
            print(f"Ошибка при отправке сообщения: {text_response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения: {e}")
        return False

    # Отправка файла по URL, если он есть
    if file_url:
        try:
            # Получаем файл из хранилища
            file_path = default_storage.path(file_url)
            with open(file_path, 'rb') as file_obj:
                file_data = {"document": file_obj}
                file_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
                
                file_response = requests.post(
                    file_url,
                    data={"chat_id": CHAT_ID},
                    files=file_data,
                    timeout=30
                )

                if file_response.status_code != 200:
                    print(f"Ошибка при отправке файла: {file_response.text}")
                    return False
                    
        except Exception as e:
            print(f"Ошибка при работе с файлом: {e}")
            return False

    return True
