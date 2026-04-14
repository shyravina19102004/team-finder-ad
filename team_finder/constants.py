"""
Константы длины полей моделей и форм.
Все max_length вынесены сюда, чтобы избежать дублирования и упростить поиск.
"""

# accounts
AVATAR_SIZE = (150, 150)
AVATAR_TEXT_COLOR = "#2C3E50"
SKILLS_AUTOCOMPLETE_LIMIT = 10
SKILL_NAME_MAX_LENGTH = 124
USER_NAME_MAX_LENGTH = 124
USER_SURNAME_MAX_LENGTH = 124
USER_PHONE_MAX_LENGTH = 12
# normalize_phone
PHONE_DIGITS_LENGTH_11 = 11
PHONE_DIGITS_LENGTH_10 = 10
PHONE_FIRST_DIGITS = ("7", "8")
PHONE_FORMATTED_PREFIX = "+7"
PHONE_VALIDATION_MESSAGE = "Формат: 8XXXXXXXXXX или +7XXXXXXXXXX (X — цифры)"
USER_ABOUT_MAX_LENGTH = 256

# базовая директория для шрифтов (может быть изменена)
FONTS_BASE_DIR = "/usr/share/fonts/truetype/"
# шрифты для аватарки (кросс-платформенные пути)
FONT_PATHS = [
    "arial.ttf",
    "Arial.ttf",
    FONTS_BASE_DIR + "dejavu/DejaVuSans.ttf",
    FONTS_BASE_DIR + "liberation/LiberationSans-Regular.ttf",
    "C:\\Windows\\Fonts\\arial.ttf",  # Windows
]

# смещение текста аватарки (для тонкой настройки)
AVATAR_TEXT_OFFSET_X = 0
AVATAR_TEXT_OFFSET_Y = -5
# координаты якоря для текста
AVATAR_ANCHOR_POINT = (0, 0)

# projects
PROJECT_NAME_MAX_LENGTH = 200
PROJECT_STATUS_MAX_LENGTH = 6
PROJECT_STATUS_OPEN = "open"
PROJECT_STATUS_CLOSED = "closed"

# pagination
PAGINATE_PER_PAGE = 12