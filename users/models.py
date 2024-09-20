from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

ADMIN = 1
PERFORMANCE = 2
CUSTOMER = 3

ROLE = (
    (ADMIN, 'АДМИН'),
    (PERFORMANCE, 'ПРОИЗВОДИТЕЛЬНОСТЬ'),
    (CUSTOMER, 'КЛИЕНТ')
)


class User(AbstractUser):
    role = models.IntegerField(verbose_name='Роль пользователя', choices=ROLE, default=CUSTOMER)
    email = models.EmailField('email', max_length=250, unique=True)
    is_active = models.BooleanField(default=True)

    @property
    def get_image(self):
        # Agar image_user bo'sh bo'lsa, None qaytaradi, aks holda birinchi tasvirni qaytaradi
        return self.image_user.first() if self.image_user.exists() else None

    @property
    def get_country(self):
        # Agar image_user bo'sh bo'lsa, None qaytaradi, aks holda birinchi tasvirni qaytaradi
        return self.country_set.all() if self.image_user.exists() else None

    @property
    def get_star(self):
        if self.supplier.exists():
            sum = 0
            for star in self.supplier.all():
                sum += star.star
            return sum // self.supplier.count()
        else:
            return None


@receiver(post_save, sender=User)
def create_user_for_profile(sender, instance, created, **kwargs):
    # Check if this is a new profile
    if created:
        # Create a user associated with the profile
        # print(instance.username)
        # user = User.objects.create(
        #     username=instance.username,  # Assuming email is used as the username
        #     first_name=instance.first_name,
        #     last_name=instance.last_name,
        #     email=instance.email
        # )
        # print(instance.password)
        # instance.set_password(instance.password)  # Set a default password or generate one
        instance.save()
        # instance.user = user  # Link the user to the profile
        # instance.save()  # Save the UserProfile with the associated user


class Profile(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    first_name = models.CharField('има', max_length=250, null=True, blank=True)
    last_name = models.CharField('фамилия', max_length=250, null=True, blank=True)
    phone = models.CharField('Номер телефона', max_length=250, null=True, blank=True)
    country = models.CharField('Страна', max_length=250, null=True, blank=True)
    city = models.CharField('Город', max_length=250, null=True, blank=True)
    description = models.TextField('О пользователе', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class ImageAvatar(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, related_name="image_user")
    image = models.ImageField(upload_to='avatar/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Изображение Аватара'
        verbose_name_plural = 'Изображение Аватара'


class Country(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE,
                             related_name='profile_countries')
    name = models.CharField('Основные направления', max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'основные направления'
        verbose_name_plural = 'основные направления'


class Help(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    question = models.TextField('вопросы', null=True, blank=True)
    answer = models.TextField('ответы', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Помощь'
        verbose_name_plural = 'Помощь'


class Like(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    user_like = models.ForeignKey(User, verbose_name='Понравившийся пользователь', on_delete=models.CASCADE,
                                  related_name='like_user')
    is_like = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Нравиться'
        verbose_name_plural = 'Нравиться'
