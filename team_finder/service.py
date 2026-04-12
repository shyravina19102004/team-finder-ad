"""Вспомогательные функции для приложений."""

import re

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator

from team_finder.constants import (
    PAGINATE_PER_PAGE,
    PHONE_DIGITS_LENGTH_10,
    PHONE_DIGITS_LENGTH_11,
    PHONE_FIRST_DIGITS,
    PHONE_FORMATTED_PREFIX,
    PHONE_VALIDATION_MESSAGE,
)


def paginate(request, queryset, per_page: int = PAGINATE_PER_PAGE):
    """
    Пагинирует queryset и возвращает page_obj и current_query для контекста шаблона.

    Args:
        request: HttpRequest (нужен для request.GET)
        queryset: QuerySet для пагинации
        per_page: количество объектов на странице

    Returns:
        dict с ключами "page_obj" и "current_query"
    """
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    current_query = request.GET.copy()
    current_query.pop("page", None)
    current_query = current_query.urlencode()

    return {"page_obj": page_obj, "current_query": current_query}


def normalize_phone(value: str) -> str:
    """Форматирование телефонного номера.

    Приводит телефон к формату +7XXXXXXXXXX.
    Допустимые входные форматы: 8XXXXXXXXXX, +7XXXXXXXXXX (X — цифры).
    При неверном формате вызывает ValidationError.
    """
    digits = re.sub(r"\D", "", str(value).strip())
    if len(digits) == PHONE_DIGITS_LENGTH_11 and digits[0] in PHONE_FIRST_DIGITS:
        return PHONE_FORMATTED_PREFIX + digits[1:]
    if len(digits) == PHONE_DIGITS_LENGTH_10:
        return PHONE_FORMATTED_PREFIX + digits
    raise ValidationError(PHONE_VALIDATION_MESSAGE)


def normalize_phone_for_comparison(value: str) -> str | None:
    return normalize_phone(value) if value else None
