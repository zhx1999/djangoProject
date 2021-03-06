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
    path('',views.login,name='login'),
    path('regist/',views.regist,name='regist'),
    path('password_reset/', views.password_reset, name='password_reset'),           # 密码找回
    path('get_verify_code/', views.get_verify_code, name='get_verify_code'),
    path('loadAllData/',views.loadAllData,name='loadAllData'),
    path('main/',views.mainView,name='main'),                                       # 主页面
    path('search/',views.search,name='search'),                                     # 分页搜索
    path('searchstate/', views.searchstate, name='searchstate'),
    path('loadSelectData/',views.loadSelectData,name='loadSelectData'),
    path('loadSearchStateData/',views.loadSearchStateData,name='loadSearchStateData'),
    path('loadSearchCityData/',views.loadSearchCityData,name='loadSearchCityData'),
    path('loadSearchCityStateData/', views.loadSearchCityStateData, name='loadSearchCityStateData'),
    path('loadSearchDtData/',views.loadSearchDtData,name='loadSearchDtData'),
    path('city_temp_state/',views.city_temp_state,name='city_temp_state'),          # 城市天气预报
    path('max_temp_state/',views.max_temp_state,name='max_temp_state'),
    path('chinaMap/',views.chinaMap,name='chinaMap'),
    path('max_ten_city/',views.max_ten_city,name='max_ten_city'),
    path('create_code_img/',views.create_code_img,name='create_code_img'),
    path('logout/',views.logout,name='logout'),
    path('modPassword/',views.modPwd,name='modPassword')

]
