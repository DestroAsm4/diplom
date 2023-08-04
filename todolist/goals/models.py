from django.db import models
from django.utils import timezone

from core.models import User


class DatesModelMixin(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(verbose_name="Дата создания", blank=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)


class Status(models.IntegerChoices):
    to_do = 1, 'К выполнению'
    in_progress = 2, 'В процессе'
    done = 3, 'Выполнено'
    archived = 4, 'Архив'


class Priority(models.IntegerChoices):
    low = 1, 'Низкий'
    medium = 2, 'Средний'
    high = 3, 'Высокий'
    critical = 4, 'Критический'


class GoalCategory(DatesModelMixin):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    board = models.ForeignKey(
        "Board", verbose_name="Доска", on_delete=models.PROTECT, related_name="categories"
    )
    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class Goal(DatesModelMixin):
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    category = models.ForeignKey(GoalCategory, verbose_name="Категория", on_delete=models.PROTECT)
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.to_do, verbose_name="Статус")
    priority = models.PositiveSmallIntegerField(choices=Priority.choices, default=Priority.medium, verbose_name="Приоритет")
    due_date = models.DateTimeField(verbose_name="Дата дедлайна", blank=True, null=True)


class GoalComment(DatesModelMixin):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    goal = models.ForeignKey(Goal, on_delete=models.PROTECT, verbose_name='Цель')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст комментария')


class Board(DatesModelMixin):
    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class BoardParticipant(DatesModelMixin):
    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    board = models.ForeignKey(
        Board,
        verbose_name="Доска",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    role = models.PositiveSmallIntegerField(
        verbose_name="Роль", choices=Role.choices, default=Role.owner
    )


