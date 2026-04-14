import random
import uuid
from enum import StrEnum
from io import BytesIO

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont

from team_finder.constants import (
    AVATAR_SIZE,
    AVATAR_TEXT_COLOR,
    AVATAR_TEXT_OFFSET_X,
    AVATAR_TEXT_OFFSET_Y,
    AVATAR_ANCHOR_POINT,
    FONT_PATHS,
    SKILL_NAME_MAX_LENGTH,
    USER_ABOUT_MAX_LENGTH,
    USER_NAME_MAX_LENGTH,
    USER_PHONE_MAX_LENGTH,
    USER_SURNAME_MAX_LENGTH,
)

from .managers import UserManager


class AvatarBackgroundColor(StrEnum):
    SOFT_BLUE = "#B8D4E3"
    SOFT_PURPLE = "#D4B8E3"
    SOFT_GREEN = "#B8E3D4"
    SOFT_BEIGE = "#E3D4B8"
    SOFT_PINK = "#E3B8B8"
    SOFT_OLIVE = "#C9D4B8"
    SOFT_TURQUOISE = "#B8D4D4"


class Skill(models.Model):
    name = models.CharField("название навыка", max_length=SKILL_NAME_MAX_LENGTH)

    class Meta:
        ordering = ["name"]
        verbose_name = "навык"
        verbose_name_plural = "навыки"

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname", "phone"]

    email = models.EmailField("адрес электронной почты", unique=True)
    name = models.CharField("имя", max_length=USER_NAME_MAX_LENGTH)
    surname = models.CharField("фамилия", max_length=USER_SURNAME_MAX_LENGTH)
    avatar = models.ImageField("аватарка", upload_to="avatars/", blank=True)
    phone = models.CharField("номер телефона", max_length=USER_PHONE_MAX_LENGTH)
    github_url = models.URLField("ссылка на Github", blank=True)
    about = models.TextField(
        "описание профиля",
        max_length=USER_ABOUT_MAX_LENGTH,
        blank=True,
    )
    is_active = models.BooleanField("активный пользователь", default=True)
    is_staff = models.BooleanField("администратор", default=False)
    skills = models.ManyToManyField(
        Skill,
        related_name="users",
        verbose_name="навыки",
        blank=True,
    )

    objects = UserManager()

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.pk is None and not self.avatar:
            self._generate_avatar()
        super().save(*args, **kwargs)

    def _get_avatar_font(self):
        for path in FONT_PATHS:
            try:
                return ImageFont.truetype(path, 72)
            except OSError:
                continue
        return ImageFont.load_default()

    def _generate_avatar(self):
        letter = self.name[0].upper() if self.name else "?"

        img = Image.new(
            "RGB",
            AVATAR_SIZE,
            random.choice(list(AvatarBackgroundColor)).value,
        )
        draw = ImageDraw.Draw(img)
        font = self._get_avatar_font()

        bbox = draw.textbbox(AVATAR_ANCHOR_POINT, letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (AVATAR_SIZE[0] - text_width) // 2 + AVATAR_TEXT_OFFSET_X
        y = (AVATAR_SIZE[1] - text_height) // 2 + AVATAR_TEXT_OFFSET_Y

        draw.text((x, y), letter, fill=AVATAR_TEXT_COLOR, font=font)

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        filename = f"{uuid.uuid4()}.png"
        self.avatar.save(filename, ContentFile(buffer.read()), save=False)
