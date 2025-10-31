# Django Tour Project

Django проект для туристического сайта с возможностью деплоя фронтенда на GitHub Pages.

## Деплой на GitHub Pages

### Автоматический деплой через GitHub Actions

1. **Настройте GitHub Pages в репозитории:**
   - Перейдите в Settings → Pages
   - В разделе "Source" выберите "GitHub Actions"

2. **Сделайте push в репозиторий:**
   - GitHub Actions автоматически сгенерирует статические файлы из Django шаблонов
   - И задеплоит их на GitHub Pages
   - Workflow запускается при push в ветку `main` или `master`

### Ручная генерация статических файлов

Если хотите протестировать локально или задеплоить вручную:

```bash
python generate_static.py
```

Скрипт создаст папку `docs/` со всеми статическими HTML файлами и статикой. После этого:
- Для локального тестирования: откройте `docs/index.html` в браузере
- Для деплоя: закоммитьте папку `docs/` и задеплойте через GitHub Pages

## Локальный запуск Django проекта

```bash
# Активируйте виртуальное окружение
venv\Scripts\activate  # Windows
# или
source venv/bin/activate  # Linux/Mac

# Запустите миграции
python manage.py migrate

# Создайте суперпользователя (опционально)
python manage.py createsuperuser

# Запустите сервер разработки
python manage.py runserver
```

Сайт будет доступен по адресу: http://127.0.0.1:8000/

## Как это работает

Скрипт `generate_static.py`:
- Конвертирует Django шаблоны в статические HTML файлы
- Заменяет `{% static %}` теги на относительные пути
- Заменяет `{% url %}` теги на относительные URL
- Копирует все статические файлы (CSS, JS, изображения) в папку `docs/static/`
- Создает структуру папок для GitHub Pages (каждая страница в своей папке с `index.html`)

