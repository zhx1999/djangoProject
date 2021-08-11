"""ProApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from dbzq import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('regist/', views.regist, name='regist'),
    path('loadAllData/', views.loadAllData, name='loadAllData'),
    path('main/', views.mainView, name='main'),
    path('search/', views.search, name='search'),
    path('searchstate/', views.searchstate, name='searchstate'),
    path('loadSelectData/', views.loadSelectData, name='loadSelectData'),
    path('loadSearchStateData/', views.loadSearchStateData, name='loadSearchStateData'),
    path('loadSearchCityData/', views.loadSearchCityData, name='loadSearchCityData'),
    path('loadSearchCityStateData/', views.loadSearchCityStateData, name='loadSearchCityStateData'),
    path('loadSearchDtData/', views.loadSearchDtData, name='loadSearchDtData'),

    path('max_temp_state/', views.max_temp_state, name='max_temp_state'),
    path('chinaMap/', views.chinaMap, name='chinaMap'),
]
