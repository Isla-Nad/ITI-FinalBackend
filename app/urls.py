"""
URL configuration for app project.

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
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings

from custom_admin.views import admin_login, admin_logout, custom_404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('accounts.urls')),
    path('clinics/', include('clinics.urls')),
    path('community/', include('community.urls')),
    path('appointments/', include('appointments.urls')),
    path('medical/', include('medical_history.urls')),
    path('custom_admin/', include('custom_admin.urls')),
    path('', admin_login, name='admin_login'),
    path('admin_logout/', admin_logout, name='admin_logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    re_path(r'^.*$', custom_404_view),
]
