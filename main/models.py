from django.db import models

from users.models import User


# Create your models here.

class FAQ(models.Model):
    question = models.TextField('вопросы', null=True, blank=True)
    answer = models.TextField('ответы', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ВОПРОСЫ-ОТВЕТЫ'
        verbose_name_plural = 'ВОПРОСЫ-ОТВЕТЫ'

    def __str__(self):
        return f"{self.pk}-{self.question}"


class RoadMapRow(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'ВОПРОСЫ-ОТВЕТЫ'
        verbose_name_plural = 'ВОПРОСЫ-ОТВЕТЫ'

    def __str__(self):
        return f"{self.pk} {self.title}"


class RoadMap(models.Model):
    q = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    row = models.ForeignKey(RoadMapRow, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = 'ВОПРОСЫ-ОТВЕТЫ'
        verbose_name_plural = 'ВОПРОСЫ-ОТВЕТЫ'

    def __str__(self):
        return f"{self.pk} {self.q}"


class FAQTwo(models.Model):
    question = models.TextField('вопросы', null=True, blank=True)
    answer = models.TextField('ответы', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Часто задаваемые вопросы'
        verbose_name_plural = 'Часто задаваемые вопросы'

    def __str__(self):
        return f"{self.pk}-{self.question}"


class LeaveARequest(models.Model):
    name = models.CharField('имя', max_length=200, null=True, blank=True)
    email = models.EmailField('E-mail', max_length=200, null=True, blank=True)
    message = models.TextField('Отиците свои вопрос', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Оставьте заявку'
        verbose_name_plural = 'Оставьте заявку'

    def __str__(self):
        return f"{self.pk}-{self.name}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notification for {self.user.username}"

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомление'


class TopSales(models.Model):
    title = models.CharField('заголовок', max_length=200, null=True, blank=True)
    subtitle = models.CharField('подзаголовок', max_length=200, null=True, blank=True)
    image = models.ImageField('изображение', upload_to='top_sale/', null=True, blank=True)
    url = models.URLField('url', max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}-{self.title}"

    class Meta:
        verbose_name = 'Топ Продаж'
        verbose_name_plural = 'Топ Продаж'
