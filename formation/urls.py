"""formation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from backend import views as back_views

urlpatterns = [
    path('', back_views.index, name="front"),
    path('connexion/', back_views.connexion, name="connexion"),
    path('deconnexion/', back_views.deconnexion, name="deconnexion"),
    path('inscription/', back_views.inscription, name="inscription"),
    path('espace/', back_views.formations, name="espace"),
    path('formations/', back_views.formations, name="formations-list"),
    path('formations/<formation_pk>/inscription/', back_views.inscription, name="form-inscription"),
    path('contact/', back_views.contact, name="contact"),
    path('admin/', admin.site.urls),
]
