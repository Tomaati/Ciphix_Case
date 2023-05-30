"""
URL configuration for CiphixInterface project.

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
from apps.dashboard_app import views as dashboard
from apps.login_app import views as login
from apps.settings_app import views as settings
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login.signin, name='login'),
    path('logout/', login.signout, name='logout'),
    path('dashboard/', dashboard.summarizing_table_graph, name='dashboard'),
    path('settings/', settings.topic_summary_table, name='settings')
]
