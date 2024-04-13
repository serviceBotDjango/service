from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django import forms

from django.contrib.auth.models import User

# Модели отображают информацию о данных, с которыми вы работаете.
# Они содержат поля и поведение ваших данных.
# Обычно одна модель представляет одну таблицу в базе данных.
# Каждая модель это класс унаследованный от django.db.models.Model.
# Атрибут модели представляет поле в базе данных.
# Django предоставляет автоматически созданное API для доступа к данным

# choices (список выбора). Итератор (например, список или кортеж) 2-х элементных кортежей,
# определяющих варианты значений для поля.
# При определении, виджет формы использует select вместо стандартного текстового поля
# и ограничит значение поля указанными значениями.

# Читабельное имя поля (метка, label). Каждое поле, кроме ForeignKey, ManyToManyField и OneToOneField,
# первым аргументом принимает необязательное читабельное название.
# Если оно не указано, Django самостоятельно создаст его, используя название поля, заменяя подчеркивание на пробел.
# null - Если True, Django сохранит пустое значение как NULL в базе данных. По умолчанию - False.
# blank - Если True, поле не обязательно и может быть пустым. По умолчанию - False.
# Это не то же что и null. null относится к базе данных, blank - к проверке данных.
# Если поле содержит blank=True, форма позволит передать пустое значение.
# При blank=False - поле обязательно.

# Пользователи Telegram
class Customer(models.Model):
    telegram_id = models.IntegerField(_('telegram_id'), unique=True)
    phone_number = models.CharField(_('phone_number'), max_length=20)    
    first_name = models.CharField(_('first_name'), max_length=64)    
    last_name = models.CharField(_('last_name'), max_length=64)   
    date_joined = models.DateTimeField(_('date_joined'))
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'customer'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['telegram_id']),
        ]
        # Сортировка по умолчанию
        ordering = ['first_name', 'last_name']
    def __str__(self):
        # Вывод 
        return "{} {}: {}".format(self.first_name, self.last_name, self.phone_number)

# Журнал работы
class Log(models.Model):
    date_log = models.DateTimeField(_('date_log'), auto_now_add=True)
    telegram_id = models.IntegerField(_('telegram_id'))
    kind = models.CharField(_('log_kind'), max_length=64)   
    event = models.TextField(_('log_event'))
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'log'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['date_log', 'telegram_id']),
        ]
        # Сортировка по умолчанию
        ordering = ['date_log']
    def __str__(self):
        # Вывод 
        return "{}: {} - {}".format(self.date_log, self.kind, self.event)

# Тип устройства
class DeviceType(models.Model):
    device_type_title = models.CharField(_('device_type_title'), max_length=128, unique=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'device_type'
    def __str__(self):
        # Вывод 
        return "{}".format(self.device_type_title)

# Производители
class Manufacturer(models.Model):
    manufacturer_title = models.CharField(_('manufacturer_title'), max_length=128, unique=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'manufacturer'
    def __str__(self):
        # Вывод 
        return "{}".format(self.manufacturer_title)

# Заявки на ремонт
class Application(models.Model):
    date_application = models.DateTimeField(_('date_application'), auto_now_add=True)
    telegram_id = models.IntegerField(_('telegram_id'))
    device_type = models.CharField(_('device_type'), max_length=96)   
    manufacturer = models.CharField(_('manufacturer'), max_length=128)   
    model = models.CharField(_('application_model'), max_length=128)   
    problem = models.TextField(_('application_problem'))
    solution = models.TextField(_('application_solution'), blank=True, null=True)
    price = models.DecimalField(_('application_price'), max_digits=9, decimal_places=2, blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'application'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['date_application', 'telegram_id']),
        ]
        # Сортировка по умолчанию
        ordering = ['date_application']
    def __str__(self):
        # Вывод 
        return "{}: {}".format(self.date_application, self.price)

# Представление Заявки на ремонт
class ViewApplication(models.Model):
    date_application = models.DateTimeField(_('date_application'))
    telegram_id = models.IntegerField(_('telegram_id'))
    phone_number = models.CharField(_('phone_number'), max_length=20)    
    first_name = models.CharField(_('first_name'), max_length=64)    
    last_name = models.CharField(_('last_name'), max_length=64)   
    date_joined = models.DateTimeField(_('date_joined'))
    device_type = models.CharField(_('device_type'), max_length=96)   
    manufacturer = models.CharField(_('manufacturer'), max_length=128)   
    model = models.CharField(_('application_model'), max_length=128)   
    problem = models.TextField(_('application_problem'))
    solution = models.TextField(_('application_solution'), blank=True, null=True)
    price = models.DecimalField(_('application_price'), max_digits=9, decimal_places=2, blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'view_application'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['date_application']),
        ]
        # Сортировка по умолчанию
        ordering = ['date_application']
        # Таблицу не надо не добавлять не удалять
        managed = False

# Заявки на заправку картриджей
class Refilling(models.Model):
    date_refilling = models.DateTimeField(_('date_refilling'), auto_now_add=True)
    telegram_id = models.IntegerField(_('telegram_id'))
    model = models.CharField(_('refilling_model'), max_length=128)   
    price = models.DecimalField(_('refilling_price'), max_digits=9, decimal_places=2, blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'refilling'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['date_refilling', 'telegram_id']),
        ]
        # Сортировка по умолчанию
        ordering = ['date_refilling']
    def __str__(self):
        # Вывод 
        return "{}: {}".format(self.date_refilling, self.price)

# Представление Заявки на заправку картриджей
class ViewRefilling(models.Model):
    date_refilling = models.DateTimeField(_('date_refilling'))
    telegram_id = models.IntegerField(_('telegram_id'))
    phone_number = models.CharField(_('phone_number'), max_length=20)    
    first_name = models.CharField(_('first_name'), max_length=64)    
    last_name = models.CharField(_('last_name'), max_length=64)   
    date_joined = models.DateTimeField(_('date_joined'))
    model = models.CharField(_('refilling_model'), max_length=128)   
    price = models.DecimalField(_('refilling_price'), max_digits=9, decimal_places=2, blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'view_refilling'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['date_refilling']),
        ]
        # Сортировка по умолчанию
        ordering = ['date_refilling']
        # Таблицу не надо не добавлять не удалять
        managed = False

# Отзывы
class Review(models.Model):
    date_review = models.DateTimeField(_('date_review'), auto_now_add=True)
    telegram_id = models.IntegerField(_('telegram_id'))
    details = models.TextField(_('review_details'))
    rating = models.IntegerField(_('rating'))
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'review'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['date_review', 'telegram_id']),
        ]
        # Сортировка по умолчанию
        ordering = ['date_review']
    def __str__(self):
        # Вывод 
        return "{}: {}".format(self.date_review, self.rating)

# Представление Заявки на заправку картриджей
class ViewReview(models.Model):
    date_review = models.DateTimeField(_('date_review'))
    telegram_id = models.IntegerField(_('telegram_id'))
    phone_number = models.CharField(_('phone_number'), max_length=20)    
    first_name = models.CharField(_('first_name'), max_length=64)    
    last_name = models.CharField(_('last_name'), max_length=64)   
    date_joined = models.DateTimeField(_('date_joined'))
    details = models.TextField(_('review_details'))
    rating = models.IntegerField(_('rating'))
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'view_review'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['date_review']),
        ]
        # Сортировка по умолчанию
        ordering = ['date_review']
        # Таблицу не надо не добавлять не удалять
        managed = False