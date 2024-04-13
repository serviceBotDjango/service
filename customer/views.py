from django.shortcuts import render, redirect

# Класс HttpResponse из пакета django.http, который позволяет отправить текстовое содержимое.
from django.http import HttpResponse, HttpResponseNotFound
# Конструктор принимает один обязательный аргумент – путь для перенаправления. Это может быть полный URL (например, 'https://www.yahoo.com/search/') или абсолютный путь без домена (например, '/search/').
from django.http import HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from django.db.models import Max
from django.db.models import Avg
from django.db.models import Q

from datetime import datetime, timedelta

# Отправка почты
from django.core.mail import send_mail

# Подключение моделей
from .models import Customer, Log, DeviceType, Manufacturer, Application, ViewApplication, Refilling, ViewRefilling, Review, ViewReview
# Подключение форм
from .forms import DeviceTypeForm, ManufacturerForm, ApplicationForm, RefillingForm, SignUpForm

from django.db.models import Sum

from django.db import models

import sys

import math

#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.contrib.auth import login as auth_login

from django.db.models.query import QuerySet

import csv
import xlwt
from io import BytesIO

# Create your views here.
# Групповые ограничения
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='403')

###################################################################################################

# Стартовая страница 
def index(request):
    try:
        return render(request, "index.html")            
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)    

# Контакты
def contact(request):
    try:
        return render(request, "contact.html")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)
    
###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def customer_index(request):
    try:
        customer = Customer.objects.all().order_by('date_joined')
        return render(request, "customer/index.html", {"customer": customer,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def customer_read(request, id):
    try:
        customer = Customer.objects.get(id=id) 
        return render(request, "customer/read.html", {"customer": customer})
    except Customer.DoesNotExist:
        return HttpResponseNotFound("<h2>Customer not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def log_index(request):
    try:
        log = Log.objects.all().order_by('-date_log')
        return render(request, "log/index.html", {"log": log,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def log_read(request, id):
    try:
        log = Log.objects.get(id=id) 
        return render(request, "log/read.html", {"log": log})
    except Log.DoesNotExist:
        return HttpResponseNotFound("<h2>Log not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def device_type_index(request):
    try:
        device_type = DeviceType.objects.all().order_by('device_type_title')
        return render(request, "device_type/index.html", {"device_type": device_type,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def device_type_create(request):
    try:
        if request.method == "POST":
            device_type = DeviceType()
            device_type.device_type_title = request.POST.get("device_type_title")
            device_typeform = DeviceTypeForm(request.POST)
            if device_typeform.is_valid():
                device_type.save()
                return HttpResponseRedirect(reverse('device_type_index'))
            else:
                return render(request, "device_type/create.html", {"form": device_typeform})
        else:        
            device_typeform = DeviceTypeForm()
            return render(request, "device_type/create.html", {"form": device_typeform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def device_type_edit(request, id):
    try:
        device_type = DeviceType.objects.get(id=id)
        if request.method == "POST":
            device_type.device_type_title = request.POST.get("device_type_title")
            device_typeform = DeviceTypeForm(request.POST)
            if device_typeform.is_valid():
                device_type.save()
                return HttpResponseRedirect(reverse('device_type_index'))
            else:
                return render(request, "device_type/edit.html", {"form": device_typeform})
        else:
            # Загрузка начальных данных
            device_typeform = DeviceTypeForm(initial={'device_type_title': device_type.device_type_title, })
            return render(request, "device_type/edit.html", {"form": device_typeform})
    except DeviceType.DoesNotExist:
        return HttpResponseNotFound("<h2>DeviceType not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def device_type_delete(request, id):
    try:
        device_type = DeviceType.objects.get(id=id)
        device_type.delete()
        return HttpResponseRedirect(reverse('device_type_index'))
    except DeviceType.DoesNotExist:
        return HttpResponseNotFound("<h2>DeviceType not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def device_type_read(request, id):
    try:
        device_type = DeviceType.objects.get(id=id) 
        return render(request, "device_type/read.html", {"device_type": device_type})
    except DeviceType.DoesNotExist:
        return HttpResponseNotFound("<h2>DeviceType not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def manufacturer_index(request):
    try:
        manufacturer = Manufacturer.objects.all().order_by('manufacturer_title')
        return render(request, "manufacturer/index.html", {"manufacturer": manufacturer,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def manufacturer_create(request):
    try:
        if request.method == "POST":
            manufacturer = Manufacturer()
            manufacturer.manufacturer_title = request.POST.get("manufacturer_title")
            manufacturerform = ManufacturerForm(request.POST)
            if manufacturerform.is_valid():
                manufacturer.save()
                return HttpResponseRedirect(reverse('manufacturer_index'))
            else:
                return render(request, "manufacturer/create.html", {"form": manufacturerform})
        else:        
            manufacturerform = ManufacturerForm()
            return render(request, "manufacturer/create.html", {"form": manufacturerform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def manufacturer_edit(request, id):
    try:
        manufacturer = Manufacturer.objects.get(id=id)
        if request.method == "POST":
            manufacturer.manufacturer_title = request.POST.get("manufacturer_title")
            manufacturerform = ManufacturerForm(request.POST)
            if manufacturerform.is_valid():
                manufacturer.save()
                return HttpResponseRedirect(reverse('manufacturer_index'))
            else:
                return render(request, "manufacturer/edit.html", {"form": manufacturerform})
        else:
            # Загрузка начальных данных
            manufacturerform = ManufacturerForm(initial={'manufacturer_title': manufacturer.manufacturer_title, })
            return render(request, "manufacturer/edit.html", {"form": manufacturerform})
    except Manufacturer.DoesNotExist:
        return HttpResponseNotFound("<h2>Manufacturer not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def manufacturer_delete(request, id):
    try:
        manufacturer = Manufacturer.objects.get(id=id)
        manufacturer.delete()
        return HttpResponseRedirect(reverse('manufacturer_index'))
    except Manufacturer.DoesNotExist:
        return HttpResponseNotFound("<h2>Manufacturer not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def manufacturer_read(request, id):
    try:
        manufacturer = Manufacturer.objects.get(id=id) 
        return render(request, "manufacturer/read.html", {"manufacturer": manufacturer})
    except Manufacturer.DoesNotExist:
        return HttpResponseNotFound("<h2>Manufacturer not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def application_index(request):
    try:
        application = ViewApplication.objects.all().order_by('date_application')
        return render(request, "application/index.html", {"application": application,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def application_edit(request, id):
    try:
        application = Application.objects.get(id=id)
        print(application.telegram_id)
        view_application = ViewApplication.objects.get(id=id)
        print(view_application.telegram_id)
        if request.method == "POST":
            application.solution = request.POST.get("solution")
            application.price = request.POST.get("price")
            applicationform = ApplicationForm(request.POST)
            if applicationform.is_valid():
                application.save()
                return HttpResponseRedirect(reverse('application_index'))
            else:
                return render(request, "application/edit.html", {"form": applicationform})
        else:
            # Загрузка начальных данных
            applicationform = ApplicationForm(initial={'solution': application.solution, 'price': application.price, 'application': application, })
            return render(request, "application/edit.html", {"form": applicationform, 'view_application': view_application,})
    except Application.DoesNotExist:
        return HttpResponseNotFound("<h2>Application not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def application_delete(request, id):
    try:
        application = Application.objects.get(id=id)
        application.delete()
        return HttpResponseRedirect(reverse('application_index'))
    except Application.DoesNotExist:
        return HttpResponseNotFound("<h2>Application not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def application_read(request, id):
    try:
        application = ViewApplication.objects.get(id=id) 
        return render(request, "application/read.html", {"application": application})
    except Application.DoesNotExist:
        return HttpResponseNotFound("<h2>Application not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def refilling_index(request):
    try:
        refilling = ViewRefilling.objects.all().order_by('date_refilling')
        return render(request, "refilling/index.html", {"refilling": refilling,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def refilling_edit(request, id):
    try:
        refilling = Refilling.objects.get(id=id)
        view_refilling = ViewRefilling.objects.get(id=id) 
        if request.method == "POST":
            refilling.price = request.POST.get("price")
            refillingform = RefillingForm(request.POST)
            if refillingform.is_valid():
                refilling.save()
                return HttpResponseRedirect(reverse('refilling_index'))
            else:
                return render(request, "refilling/edit.html", {"form": refillingform})
        else:
            # Загрузка начальных данных
            refillingform = RefillingForm(initial={'price': refilling.price, 'refilling': refilling, })
            return render(request, "refilling/edit.html", {"form": refillingform, 'view_refilling': view_refilling,} )
    except Refilling.DoesNotExist:
        return HttpResponseNotFound("<h2>Refilling not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def refilling_delete(request, id):
    try:
        refilling = Refilling.objects.get(id=id)
        refilling.delete()
        return HttpResponseRedirect(reverse('refilling_index'))
    except Refilling.DoesNotExist:
        return HttpResponseNotFound("<h2>Refilling not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def refilling_read(request, id):
    try:
        refilling = ViewRefilling.objects.get(id=id) 
        return render(request, "refilling/read.html", {"refilling": refilling})
    except Refilling.DoesNotExist:
        return HttpResponseNotFound("<h2>Refilling not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def review_index(request):
    try:
        review = ViewReview.objects.all().order_by('date_review')
        return render(request, "review/index.html", {"review": review,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def review_delete(request, id):
    try:
        review = Review.objects.get(id=id)
        review.delete()
        return HttpResponseRedirect(reverse('review_index'))
    except Review.DoesNotExist:
        return HttpResponseNotFound("<h2>Review not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def review_read(request, id):
    try:
        review = ViewReview.objects.get(id=id) 
        return render(request, "review/read.html", {"review": review})
    except Review.DoesNotExist:
        return HttpResponseNotFound("<h2>Review not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)
###################################################################################################

# Отчет 1
@login_required
@group_required("Managers")
def report_1(request):
    try:
        where = ""
        start_date = datetime(datetime.now().year, 1, 1, 0, 0).strftime('%Y-%m-%d') 
        finish_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0).strftime('%Y-%m-%d') 
        total = Customer.objects.all().count()
        if request.method == "POST":
            # Определить какая кнопка нажата
            if 'searchBtn' in request.POST:
                # Поиск по дате
                start_date = request.POST.get("start_date")
                #print(start_date)
                finish_date = request.POST.get("finish_date")
                finish_date = str(datetime.strptime(finish_date, "%Y-%m-%d") + timedelta(days=1))
                total = Customer.objects.filter(date_joined__range=[start_date, finish_date]).count()
                #print(finish_date)
                if where != "":
                    where = where + " AND "
                where = "customer.date_joined>='" + start_date + "' AND customer.date_joined<='" + finish_date + "'"
                print(where)
                finish_date = request.POST.get("finish_date")
                # Добавить ключевое слово WHERE 
                if where != "":
                    where = " WHERE " + where + " "              
                print(where)
# SQLite
#        report = Customer.objects.raw("""
#SELECT 1 as id, strftime('%Y', date_joined) AS year, strftime('%m', date_joined) AS month, COUNT(*) AS joined
#FROM customer
#""" 
#+ where +
#"""
#GROUP BY strftime('%Y', date_joined), strftime('%m', date_joined)
#""")
# PostgreSQL
        report = Customer.objects.raw("""
SELECT 1 as id, date_part('year', date_joined) AS year, date_part('month', date_joined) AS month, COUNT(*) AS joined
FROM customer
""" 
+ where +
"""
GROUP BY date_part('year', date_joined), date_part('month', date_joined)
ORDER BY date_part('year', date_joined), date_part('month', date_joined)
""")
        labels = []
        data = []
        # перебираем полученные строки
        for row in report:
            labels.append(row.month)
            data.append(int(row.joined))
        #print(labels)
        #print(data)
        return render(request, "report/report_1.html", {"report": report, "total": total, "start_date": start_date, "finish_date": finish_date, "labels": labels, "data": data,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Отчет 2
@login_required
@group_required("Managers")
def report_2(request):
    try:
        where = ""
        start_date = datetime(datetime.now().year, 1, 1, 0, 0).strftime('%Y-%m-%d') 
        finish_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0).strftime('%Y-%m-%d') 
        total = Application.objects.all().count()
        if request.method == "POST":
            # Определить какая кнопка нажата
            if 'searchBtn' in request.POST:
                # Поиск по дате
                start_date = request.POST.get("start_date")
                #print(start_date)
                finish_date = request.POST.get("finish_date")
                finish_date = str(datetime.strptime(finish_date, "%Y-%m-%d") + timedelta(days=1))
                total = Application.objects.filter(date_application__range=[start_date, finish_date]).count()
                #print(finish_date)
                if where != "":
                    where = where + " AND "
                where = "application.date_application>='" + start_date + "' AND application.date_application<='" + finish_date + "'"
                print(where)
                finish_date = request.POST.get("finish_date")
                # Добавить ключевое слово WHERE 
                if where != "":
                    where = " WHERE " + where + " "              
                print(where)
# SQLite
#        report = Application.objects.raw("""
#SELECT 1 as id, strftime('%Y', date_application) AS year, strftime('%m', date_application) AS month, COUNT(*) AS application
#FROM application
#""" 
#+ where +
#"""
#GROUP BY strftime('%Y', date_application), strftime('%m', date_application)
#""")
# PostgreSQL
        report = Application.objects.raw("""
SELECT 1 as id, date_part('year', date_application) AS year, date_part('month', date_application) AS month, COUNT(*) AS application
FROM application
""" 
+ where +
"""
GROUP BY date_part('year', date_application), date_part('month', date_application)
ORDER BY date_part('year', date_application), date_part('month', date_application)
""")
        labels = []
        data = []
        # перебираем полученные строки
        for row in report:
            labels.append(row.month)
            data.append(int(row.application))
        #print(labels)
        #print(data)
        return render(request, "report/report_2.html", {"report": report, "total": total, "start_date": start_date, "finish_date": finish_date, 'labels': labels, 'data': data,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Отчет 3
@login_required
@group_required("Managers")
def report_3(request):
    try:
        where = ""
        start_date = datetime(datetime.now().year, 1, 1, 0, 0).strftime('%Y-%m-%d') 
        finish_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0).strftime('%Y-%m-%d') 
        total = Refilling.objects.all().count()
        if request.method == "POST":
            # Определить какая кнопка нажата
            if 'searchBtn' in request.POST:
                # Поиск по дате
                start_date = request.POST.get("start_date")
                #print(start_date)
                finish_date = request.POST.get("finish_date")
                finish_date = str(datetime.strptime(finish_date, "%Y-%m-%d") + timedelta(days=1))
                total = Refilling.objects.filter(date_refilling__range=[start_date, finish_date]).count()
                #print(finish_date)
                if where != "":
                    where = where + " AND "
                where = "refilling.date_refilling>='" + start_date + "' AND refilling.date_refilling<='" + finish_date + "'"
                print(where)
                finish_date = request.POST.get("finish_date")
                # Добавить ключевое слово WHERE 
                if where != "":
                    where = " WHERE " + where + " "              
                print(where)
# SQLite
#        report = Refilling.objects.raw("""
#SELECT 1 as id, strftime('%Y', date_refilling) AS year, strftime('%m', date_refilling) AS month, COUNT(*) AS refilling
#FROM refilling
#""" 
#+ where +
#"""
#GROUP BY strftime('%Y', date_refilling), strftime('%m', date_refilling)
#""")
# PostgreSQL
        report = Refilling.objects.raw("""
SELECT 1 as id, date_part('year', date_refilling) AS year, date_part('month', date_refilling) AS month, COUNT(*) AS refilling
FROM refilling
""" 
+ where +
"""
GROUP BY date_part('year', date_refilling), date_part('month', date_refilling)
ORDER BY date_part('year', date_refilling), date_part('month', date_refilling)
""")
        labels = []
        data = []
        # перебираем полученные строки
        for row in report:
            labels.append(row.month)
            data.append(int(row.refilling))
        #print(labels)
        #print(data)
        return render(request, "report/report_3.html", {"report": report, "total": total, "start_date": start_date, "finish_date": finish_date, 'labels': labels, 'data': data,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Отчет 4
@login_required
@group_required("Managers")
def report_4(request):
    try:
        where = ""
        start_date = datetime(datetime.now().year, 1, 1, 0, 0).strftime('%Y-%m-%d') 
        finish_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0).strftime('%Y-%m-%d') 
        total = Review.objects.all().count()
        avg = Review.objects.aggregate(Avg('rating'))
        print(avg['rating__avg'])
        if request.method == "POST":
            # Определить какая кнопка нажата
            if 'searchBtn' in request.POST:
                # Поиск по дате
                start_date = request.POST.get("start_date")
                #print(start_date)
                finish_date = request.POST.get("finish_date")
                finish_date = str(datetime.strptime(finish_date, "%Y-%m-%d") + timedelta(days=1))
                total = Review.objects.filter(date_review__range=[start_date, finish_date]).count()
                avg = Review.objects.filter(date_review__range=[start_date, finish_date]).aggregate(Avg('rating'))
                #print(finish_date)
                if where != "":
                    where = where + " AND "
                where = "review.date_review>='" + start_date + "' AND review.date_review<='" + finish_date + "'"
                print(where)
                finish_date = request.POST.get("finish_date")
                # Добавить ключевое слово WHERE 
                if where != "":
                    where = " WHERE " + where + " "              
                print(where)
# SQLite
#        report = Review.objects.raw("""
#SELECT 1 as id, strftime('%Y', date_review) AS year, strftime('%m', date_review) AS month, COUNT(*) AS review, AVG(rating) AS avg_rating
#FROM review
#""" 
#+ where +
#"""
#GROUP BY strftime('%Y', date_review), strftime('%m', date_review)
#""")
# PostgreSQL
        report = Review.objects.raw("""
SELECT 1 as id, date_part('year', date_review) AS year, date_part('month', date_review) AS month, COUNT(*) AS review, AVG(rating) AS avg_rating
FROM review
""" 
+ where +
"""
GROUP BY date_part('year', date_review), date_part('month', date_review)
ORDER BY date_part('year', date_review), date_part('month', date_review)
""")
        labels = []
        data = []
        # перебираем полученные строки
        for row in report:
            labels.append(row.month)
            data.append(int(row.review))
        #print(labels)
        #print(data)
        return render(request, "report/report_4.html", {"report": report, "total": total, "avg": avg, "start_date": start_date, "finish_date": finish_date, 'labels': labels, 'data': data,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)


###################################################################################################

# Регистрационная форма 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
            #return render(request, 'registration/register_done.html', {'new_user': user})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Изменение данных пользователя
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'registration/my_account.html'
    success_url = reverse_lazy('index')
    #success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user

# Выход
from django.contrib.auth import logout
def logoutUser(request):
    logout(request)
    return render(request, "index.html")

