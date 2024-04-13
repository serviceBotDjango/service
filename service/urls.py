"""
URL configuration for service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from django.conf import settings 
from django.conf.urls.static import static 
from django.conf.urls import include

from customer import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index),
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),

    path('customer/index/', views.customer_index, name='customer_index'),
    #path('customer/create/', views.customer_create, name='customer_create'),
    #path('customer/edit/<int:id>/', views.customer_edit, name='customer_edit'),
    #path('customer/delete/<int:id>/', views.customer_delete, name='customer_delete'),
    path('customer/read/<int:id>/', views.customer_read, name='customer_read'),
    
    path('log/index/', views.log_index, name='log_index'),
    #path('log/create/', views.log_create, name='log_create'),
    #path('log/edit/<int:id>/', views.log_edit, name='log_edit'),
    #path('log/delete/<int:id>/', views.log_delete, name='log_delete'),
    path('log/read/<int:id>/', views.log_read, name='log_read'),

    path('device_type/index/', views.device_type_index, name='device_type_index'),
    path('device_type/create/', views.device_type_create, name='device_type_create'),
    path('device_type/edit/<int:id>/', views.device_type_edit, name='device_type_edit'),
    path('device_type/delete/<int:id>/', views.device_type_delete, name='device_type_delete'),
    path('device_type/read/<int:id>/', views.device_type_read, name='device_type_read'),

    path('manufacturer/index/', views.manufacturer_index, name='manufacturer_index'),
    path('manufacturer/create/', views.manufacturer_create, name='manufacturer_create'),
    path('manufacturer/edit/<int:id>/', views.manufacturer_edit, name='manufacturer_edit'),
    path('manufacturer/delete/<int:id>/', views.manufacturer_delete, name='manufacturer_delete'),
    path('manufacturer/read/<int:id>/', views.manufacturer_read, name='manufacturer_read'),

    path('application/index/', views.application_index, name='application_index'),
    #path('application/create/', views.application_create, name='application_create'),
    path('application/edit/<int:id>/', views.application_edit, name='application_edit'),
    path('application/delete/<int:id>/', views.application_delete, name='application_delete'),
    path('application/read/<int:id>/', views.application_read, name='application_read'),

    path('refilling/index/', views.refilling_index, name='refilling_index'),
    #path('refilling/create/', views.refilling_create, name='refilling_create'),
    path('refilling/edit/<int:id>/', views.refilling_edit, name='refilling_edit'),
    path('refilling/delete/<int:id>/', views.refilling_delete, name='refilling_delete'),
    path('refilling/read/<int:id>/', views.refilling_read, name='refilling_read'),

    path('review/index/', views.review_index, name='review_index'),
    #path('review/create/', views.review_create, name='review_create'),
    #path('review/edit/<int:id>/', views.review_edit, name='review_edit'),
    path('review/delete/<int:id>/', views.review_delete, name='review_delete'),
    path('review/read/<int:id>/', views.review_read, name='review_read'),

    path('report/report_1/', views.report_1, name='report_1'),
    path('report/report_2/', views.report_2, name='report_2'),
    path('report/report_3/', views.report_3, name='report_3'),
    path('report/report_4/', views.report_4, name='report_4'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', views.logoutUser, name="logout"),
    path('settings/account/', views.UserUpdateView.as_view(), name='my_account'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



