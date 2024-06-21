# DevastorSaveDialogues_ChatGPT
Скриптик для сохранения диалогов с картинками в веб-интерфейсе ChatGPT

## Описание

Этот проект представляет собой скрипт на Python, который позволяет сохранять диалоги из веб-приложения ChatGPT. Скрипт использует Selenium и undetected_chromedriver для автоматического входа в аккаунт, навигации по страницам и сохранения содержимого диалогов в HTML-формате с поддержкой встроенных изображений и кода.

## Особенности

- Автоматический вход в аккаунт ChatGPT
- Сохранение текста, кода и изображений из диалогов
- Поддержка HTML-формата для сохранения диалогов
- Настроенные стили для отображения сохраненных диалогов в стиле оригинального интерфейса ChatGPT

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/ваш_профиль/DevastorDialogueSaver.git
    cd DevastorDialogueSaver
    ```

2. Установите необходимые зависимости:

    ```bash
    pip install -r requirements.txt
    ```

3. Создайте файл `credentials.txt` в корне проекта и добавьте туда свои учетные данные для входа в ChatGPT:

    ```text
    ваш_email
    ваш_пароль
    ```

## Использование

1. Запустите скрипт:

    ```bash
    python DevastorSaveGPTDialogue.py
    ```

2. Войдите в аккаунт ChatGPT в открывшемся браузере и перейдите к нужному диалогу.
3. Нажмите Enter в консоли, чтобы продолжить выполнение скрипта.

Скрипт автоматически сохранит диалог в папке `Диалог` вместе с вложениями.

## Пример HTML-структуры

Вот пример того, как будет выглядеть сохраненный HTML-файл:

```html
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
        .user-message { color: #ececec !important; background-color: #2f2f2f !important; padding: 10px; border-radius: 8px; margin-bottom: 10px; }
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

