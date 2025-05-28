from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Тег")
    
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение", blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория"
    )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ('question', 'Вопрос о товаре'),
        ('delivery', 'Доставка'),
        ('other', 'Другое'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField('Ваше имя', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email')
    feedback_type = models.CharField('Тип обращения', max_length=20, choices=FEEDBACK_TYPES)
    message = models.TextField('Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        return f"Обращение от {self.name} ({self.get_feedback_type_display()})"