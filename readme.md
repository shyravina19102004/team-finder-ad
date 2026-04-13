# TeamFinder
# TeamFinder

## О проекте

**TeamFinder** — это веб-платформа для поиска единомышленников и совместной работы над pet-проектами. Разработчики, дизайнеры, аналитики и другие специалисты могут публиковать идеи проектов, находить команду, откликаться на предложения, а также демонстрировать свои навыки.

### Основные возможности (вариант 2: «Навыки»)

- Регистрация и аутентификация пользователей (email + пароль).
- Создание, редактирование, завершение проектов.
- Управление личным профилем: аватар, контакты, описание.
- **Блок «Навыки»** в профиле пользователя:
  - Добавление/удаление навыков (тегов) через автодополнение.
  - Создание новых навыков прямо из интерфейса.
  - Изменения без перезагрузки страницы (AJAX).
- **Фильтрация пользователей по навыкам** на странице `/users/list/`.
- Пагинация (12 элементов на страницу).
- Разграничение прав: гость, авторизованный пользователь, администратор.
- Административная панель Django для управления пользователями, проектами и навыками.

> Проект выполнен в рамках дипломной работы Яндекс.Практикума.

## Стек технологий

- **Backend:** Python 3.11+, Django 5.2.4
- **База данных:** PostgreSQL 16 (или SQLite для локальной разработки)
- **ORM:** Django ORM с оптимизацией запросов (select_related, annotate)
- **Frontend:** HTML, CSS, JavaScript (готовые шаблоны, кастомные стили)
- **Управление зависимостями:** pip + requirements.txt
- **Контейнеризация:** Docker, Docker Compose
- **Переменные окружения:** python-decouple
- **Генерация аватарок:** Pillow
- **Дополнительно:** isort (сортировка импортов), flake8 (PEP8)

## Установка и запуск

### Требования

- Python 3.11 или выше
- pip
- (опционально) Docker и Docker Compose для PostgreSQL
- (опционально) Git

### Шаг 1. Клонирование репозитория

```bash
git clone https://github.com/shyravina19102004/team-finder-ad.git
cd team-finder-ad

## Развёртывание проекта

### 1. Виртуальное окружение

```bash
python3 -m venv venv
```

**Активация:**
- **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
- **Windows (cmd):** `venv\Scripts\activate`
- **Linux / macOS:** `source venv/bin/activate`

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Переменные окружения (.env)

Скопируйте пример и отредактируйте:

```bash
cp .env_example .env
```

| Переменная | Описание |
|------------|----------|
| `DJANGO_SECRET_KEY` | Секретный ключ Django (для подписи сессий, cookie). Можно сгенерировать: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DJANGO_DEBUG` | Режим отладки: `True` — для разработки |
| `POSTGRES_DB` | Имя базы данных PostgreSQL |
| `POSTGRES_USER` | Пользователь PostgreSQL |
| `POSTGRES_PASSWORD` | Пароль пользователя |
| `POSTGRES_HOST` | Хост БД (обычно `localhost`) |
| `POSTGRES_PORT` | Порт PostgreSQL (по умолчанию `5432`) |
| `TASK_VERSION` | Вариант шаблонов: `1`, `2` или `3` (папки `templates_var1`, `templates_var2`, `templates_var3`) |

### 4. База данных PostgreSQL

Запуск через Docker:

```bash
docker compose up -d
```

Остановка:

```bash
docker compose down
```

> Если порт 5432 занят, измените его в `docker-compose.yml` (например, `"5433:5432"`) и укажите тот же порт в `.env`.

### 5. Миграции и запуск

```bash
python manage.py migrate
python manage.py runserver
```

Приложение будет доступно по адресу [http://localhost:8000](http://localhost:8000).

---

## Локальная разработка без PostgreSQL

Для быстрого старта можно использовать SQLite:

```bash
python manage.py runserver --settings=team_finder.settings_local
```

В этом случае `.env` с настройками PostgreSQL не требуется. Будут использованы значения по умолчанию для `SECRET_KEY` и `TASK_VERSION`.

---

### Автор
Шуравина Оксана