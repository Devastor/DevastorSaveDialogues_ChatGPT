import os
import time
import requests
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Чтение учетных данных из файла
with open('credentials.txt', 'r', encoding='utf-8') as f:
    credentials = f.read().splitlines()
email = credentials[0]
password = credentials[1]

# Настройка undetected_chromedriver
options = ChromeOptions()
# options.headless = True  # Если нужно включить headless-режим, раскомментируйте эту строку
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

with Chrome(options=options) as driver:
    # Открытие страницы для аутентификации
    driver.get('https://chat.openai.com/')

    # Ожидание и нажатие на кнопку
    wait = WebDriverWait(driver, 10)
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[1]/div/div/button[1]/div/span')))
    login_button.click()

    # Ввод логина
    email_field = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/main/section/div[2]/div[1]/input')))
    email_field.send_keys(email)
    next_button = driver.find_element(By.XPATH, '/html/body/div/div/main/section/div[2]/button')
    next_button.click()

    # Ввод пароля
    password_field = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/section/div/div/div/form/div[1]/div/div[2]/div/input')))
    password_field.send_keys(password)
    login_button = driver.find_element(By.XPATH, '/html/body/div[1]/main/section/div/div/div/form/div[2]/button')
    login_button.click()

    # Ожидание подтверждения и продолжение
    input("Выберите нужный диалог и нажмите Enter для продолжения...")

    # Создание папок для сохранения данных
    if not os.path.exists('Диалог'):
        os.makedirs('Диалог/Вложения')

    # Функция для сохранения текста сообщения
    def save_text(message, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(message)

    # Функция для скачивания файла по URL
    def download_file(url, dest_path):
        response = requests.get(url)
        with open(dest_path, 'wb') as f:
            f.write(response.content)

    # Функция для добавления элемента в HTML
    def add_html_element(tag, content, attrs=""):
        return f"<{tag} {attrs}>{content}</{tag}>"

    # Создание основного HTML файла
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Диалог</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/styles/default.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/highlight.min.js"></script>
        <script>
            hljs.highlightAll();

            function copyCode(button) {
                const code = button.parentElement.querySelector('code').innerText;
                navigator.clipboard.writeText(code);
                button.innerText = 'Скопировано';
                setTimeout(() => { button.innerText = 'Копировать'; }, 2000);
            }

            function showModal(imageSrc) {
                const modal = document.getElementById('imageModal');
                const modalImg = document.getElementById('modalImg');
                modal.style.display = 'block';
                modalImg.src = imageSrc;
            }

            function closeModal() {
                const modal = document.getElementById('imageModal');
                modal.style.display = 'none';
            }
        </script>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; background-color: #212121; color: #d1d5da; }
            .user-message { color: #ececec !important; background-color: #2f2f2f !important; padding: 10px; border-radius: 8px; margin-bottom: 10px; margin-left: auto; max-width: 70%; }
            .ai-message { color: #ececec !important; background-color: #212121; padding: 10px; border-radius: 8px; margin-bottom: 10px; }
            .message-container { margin-bottom: 20px; }
            .code-block { background-color: #000000 !important; border-left: 4px solid #00aaff; padding: 10px; position: relative; border-radius: 5px; }
            .code-block code { display: block;  background-color: #000000 !important; color: #f8f8f2; }
            .copy-button { position: absolute; top: 10px; right: 10px; padding: 5px; background-color: #444654; border-radius: 8px; border: 1px solid #ccc; cursor: pointer; }
            .image-container { width: 200px; display: inline-block; margin: 10px; }
            .image-container img { width: 100%; cursor: pointer; border-radius: 5px; }
            .image-modal { display: none; position: fixed; z-index: 1000; padding-top: 100px; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.9); }
            .image-modal-content { margin: auto; display: block; width: 80%; max-width: 700px; border-radius: 5px; }
            .image-modal-content, .image-modal { animation-name: zoom; animation-duration: 0.6s; }
            @keyframes zoom { from { transform: scale(0) } to { transform: scale(1) } }
            .close { position: absolute; top: 50px; right: 35px; color: #f1f1f1; font-size: 40px; font-weight: bold; transition: 0.3s; }
            .close:hover, .close:focus { color: #bbb; text-decoration: none; cursor: pointer; }
        </style>
    </head>
    <body>
    <div id="imageModal" class="image-modal">
        <span class="close" onclick="closeModal()">&times;</span>
        <img class="image-modal-content" id="modalImg">
    </div>
    """

    # Инициализация счетчиков
    total_messages = 0
    user_messages = 0
    ai_messages = 0
    skipped_msg = 0

    # Сбор всех сообщений
    messages = driver.find_elements(By.XPATH, '//div[contains(@class, "group") and contains(@class, "flex") and not(contains(@class, "h-48"))]')
    for idx, message in enumerate(messages):
        if not message.text.strip():
            skipped_msg += 1
            continue  # Пропускаем пустые сообщения

        total_messages += 1

        role = ""
        # Проверка, является ли автор сообщения пользователем или ИИ
        try:
            author_role_element = message.find_element(By.XPATH, './/div[@data-message-author-role]')
            author_role = author_role_element.get_attribute('data-message-author-role')
            if author_role == 'user':
                user_messages += 1
                role = "Пользователь"
                role_class = "user-message"
            elif author_role == 'assistant':
                ai_messages += 1
                role = "ИИ"
                role_class = "ai-message"
            else:
                continue  # Пропускаем неизвестные роли
        except:
            continue  # Пропускаем сообщения без атрибута data-message-author-role

        # Заменяем роль на значок для ИИ
        if role == "ИИ":
            role_icon = "<img src='../GPT_icon.png' alt='ChatGPT Icon' width='20' height='20'>"
            role_html = f"<p>{role_icon}</p>"
        else:
            role_html = ""

        html_content += f"<div class='message-container'><div class='{role_class}'>{role_html}"

        # Сохранение текста и кода
        text_elements = message.find_elements(By.XPATH, './/div[contains(@class, "whitespace-pre-wrap")]')
        if text_elements:
            text_content = text_elements[0].text
            save_text(text_content, f'Диалог/message_{idx}.txt')

            code_elements = message.find_elements(By.XPATH, './/code[contains(@class, "!whitespace-pre hljs")]')
            if code_elements:
                for code_element in code_elements:
                    code_content = code_element.text
                    save_text(code_content, f'Диалог/code_{idx}.txt')
                    text_content = text_content.replace(code_content, f"<div class='code-block'><button class='copy-button' onclick='copyCode(this)'>Копировать</button><pre><code>{code_content}</code></pre></div>")

            html_content += f"<p>{text_content}</p>"
            print(f"Сообщение {idx - skipped_msg} сохранено (Текст: 1, Код: {len(code_elements)}", end=", ")

        # Сохранение изображений
        img_elements = message.find_elements(By.TAG_NAME, 'img')
        if img_elements:
            for img_idx, img_element in enumerate(img_elements):
                img_url = img_element.get_attribute('src')
                img_path = f'Вложения/image_{idx}_{img_idx}.png'
                download_file(img_url, f'Диалог/{img_path}')
                html_content += f"<div class='image-container'><img src='{img_path}' onclick='showModal(\"{img_path}\")'></div>"
            print(f"Изображения: {len(img_elements)}", end=", ")
        else:
            print(f"Изображения: 0", end=", ")

        # Сохранение прикрепленных файлов
        file_elements = message.find_elements(By.XPATH, './/a[contains(@href, "/attachment")]')
        if file_elements:
            for file_element in file_elements:
                file_url = file_element.get_attribute('href')
                file_name = file_element.text
                file_path = f'Вложения/{file_name}'
                download_file(file_url, f'Диалог/{file_path}')
                html_content += f"<a href='{file_path}'>{file_name}</a>"
            print(f"Файлы: {len(file_elements)})")
        else:
            print(f"Файлы: 0)")

        html_content += "</div></div>"

# Закрытие HTML структуры
html_content += """
</body>
</html>
"""

# Сохранение основного HTML файла
with open('Диалог/диалог.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

# Вывод статистики
print(f"Всего сообщений: {total_messages}")
print(f"Сообщений пользователя: {user_messages}")
print(f"Сообщений ИИ: {ai_messages}")

print("Диалог сохранен.")
