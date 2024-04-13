from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, NumberInput, DateTimeInput, CheckboxInput
from .models import DeviceType, Manufacturer, Application, Refilling
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
import pytz

# При разработке приложения, использующего базу данных, чаще всего необходимо работать с формами, которые аналогичны моделям.
# В этом случае явное определение полей формы будет дублировать код, так как все поля уже описаны в модели.
# По этой причине Django предоставляет вспомогательный класс, который позволит вам создать класс Form по имеющейся модели
# атрибут fields - указание списка используемых полей, при fields = '__all__' - все поля
# атрибут widgets для указания собственный виджет для поля. Его значением должен быть словарь, ключами которого являются имена полей, а значениями — классы или экземпляры виджетов.

# Тип устройства
class DeviceTypeForm(forms.ModelForm):
    class Meta:
        model = DeviceType
        fields = ['device_type_title',]
        widgets = {
            'device_type_title': TextInput(attrs={"size":"100"}),            
        }

# Производители
class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['manufacturer_title',]
        widgets = {
            'manufacturer_title': TextInput(attrs={"size":"100"}),            
        }

# Заявки на ремонт (только изменение)
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['solution', 'price',]
        widgets = {
            'solution': Textarea(attrs={'cols': 100, 'rows': 5}),                        
            'price': NumberInput(attrs={"size":"10", "min": "1", "step": "1"}),
        }
       
# Заявки на заправку картриджей (только изменение)
class RefillingForm(forms.ModelForm):
    class Meta:
        model = Refilling
        fields = ['price',]
        widgets = {
            'price': NumberInput(attrs={"size":"10", "min": "1", "step": "1"}),
        }

# Форма регистрации
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
