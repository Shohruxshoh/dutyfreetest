from django.db import models
from users.models import User


# Create your models here.

class Category(models.Model):
    title = models.CharField('Наименование', max_length=250, null=True, blank=True)
    is_age_limit = models.BooleanField('Возрастное ограничение', default=False)
    is_navbar = models.BooleanField('Если выбрано, оно будет отображаться', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'

    def __str__(self):
        return f"{self.pk}- {self.title}"


class Brand(models.Model):
    name = models.CharField('Наименование', max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренд'

    def __str__(self):
        return f"{self.pk}- {self.name}"


class TypeAlcohol(models.Model):
    type = models.CharField('Тип', max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = 'Тип Алкоголь'
        verbose_name_plural = 'Тип Алкоголь'

    def __str__(self):
        return f"{self.pk}-{self.type}"


class CountryOfOrigin(models.Model):
    country = models.CharField('Страна происхождения', max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = 'Страна происхождения'
        verbose_name_plural = 'Страна происхождения'

    def __str__(self):
        return f"{self.pk}-{self.country}"


for_her = '1'
for_him = '2'
for_everyone = '3'

For_whom = (
    (for_her, 'Для нее'),
    (for_him, 'Для него'),
    (for_everyone, 'для всех'),
)


class Product(models.Model):
    CURRENCY = (
        ('$', '$'),
        ('€', '€'),
        ('£', '£'),
        ('¥', '¥')
    )

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, verbose_name='Бренд', on_delete=models.SET_NULL, null=True, blank=True)
    type_alcohol = models.ForeignKey(TypeAlcohol, verbose_name='Тип Алкоголь', on_delete=models.SET_NULL, null=True,
                                     blank=True)
    country_of_origin = models.ForeignKey(CountryOfOrigin, verbose_name='Страна происхождения',
                                          on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField('Наименование', max_length=250, null=True, blank=True)
    description = models.TextField('Описание товара', null=True, blank=True)
    price = models.DecimalField('Установка цены', max_digits=10, decimal_places=2)
    currency = models.CharField('валюта', max_length=20, choices=CURRENCY, default='$')
    for_whom = models.CharField('для кого', max_length=20, choices=For_whom, default=for_everyone)
    discount_percent = models.PositiveBigIntegerField('скидка процент', default=0, help_text='Ex:10')
    is_discount = models.BooleanField('скидка', default=False)
    is_active = models.BooleanField('активный', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукт'

    def __str__(self):
        return f"{self.pk}- {self.title}"

    @property
    def discount_calculation(self):
        if self.discount_percent > 0:
            discount_price = float(self.price) * ((100 - self.discount_percent) / 100)
            return discount_price
        return self.discount_percent


class AdditionalInformation(models.Model):
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)
    for_whom = models.CharField('Для кого', max_length=250, null=True, blank=True)
    type_vial = models.CharField('Тип флакона', max_length=250, null=True, blank=True)
    aromatic = models.CharField('Ароматы', max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Дополнительная информация'
        verbose_name_plural = 'Дополнительная информация'

    def __str__(self):
        return f"{self.pk}- {self.product}-{self.for_whom}"


class Service(models.Model):
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)
    description = models.TextField('О работе сервиса', null=True, blank=True)

    class Meta:
        verbose_name = 'О работе сервиса'
        verbose_name_plural = 'О работе сервиса'

    def __str__(self):
        return f"{self.pk}- {self.product}-{self.description}"


class Image(models.Model):
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)
    image = models.ImageField('изображение', upload_to="product/")

    class Meta:
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображение продукта'

    def __str__(self):
        return f"{self.pk}- {self.product}"


class SaveProduct(models.Model):
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Сохранить продукт'
        verbose_name_plural = 'Сохранить продукт'

    def __str__(self):
        return f"{self.pk}-{self.user}-{self.product}"
