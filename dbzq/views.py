import random

from django.core.cache import cache
from django.core.mail import send_mail

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from flask import url_for

from dbzq import models
from django.core.paginator import Paginator
from django.core import serializers
from tools import checkCode
from io import BytesIO
import json


# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('name')
        password = request.POST.get('password')
        vcode = request.POST.get('check_code')
        vcodehide = request.session['check_code']

        if vcode.lower() == vcodehide.lower():
            # 条件查询
            try:
                user = models.RegistUser.objects.get(username=username)
            except:
                return render(request, 'login.html', {'msg': '登录失败，用户名不存在！'})
            if user.password == password:
                request.session['username'] = username
                return render(request, 'main.html')
            else:
                return render(request, 'login.html', {'msg': '登录失败，密码错误！'})
        else:
            return render(request, 'login.html', {'msg': '登陆失败，验证码错误！'})


def regist(request):
    if request.method == 'GET':
        return render(request, 'regist.html')
    else:
        # 表单数据的捕获
        username = request.POST.get('name')
        vcode = request.POST.get('check_code')
        vcodehide = request.session['check_code']
        if vcode.lower() == vcodehide.lower():
            try:
                user = models.RegistUser.objects.get(username=username)
                if user is not None:
                    return render(request, 'regist.html', {'msg': '注册失败，用户名已存在！'})
            except:
                password = request.POST.get('password')
                repeatpwd = request.POST.get('repeatpwd')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                if password != repeatpwd:
                    return render(request, 'regist.html', {'msg': '注册失败！两次密码不一致......'})
                else:
                    user = models.RegistUser(username=username, password=password, email=email, phone=phone)
                    user.save()
                    return render(request, 'registRight.html')
        else:
            return render(request, 'regist.html', {'msg': '注册失败，验证码错误！'})


def create_code_img(request):
    f = BytesIO()  # 在内存中临时存放验证码图片

    img, code = checkCode.create_validate_code()  # 生成 图片,验证码

    request.session['check_code'] = code  # 将验证码存在服务器的session中，用于校验
    img.save(f, 'PNG')  # 生成的图片放置于开辟的内存中

    return HttpResponse(f.getvalue())  # 将内存的数据读取出来，并以HttpResponse返回


def mainView(request):
    return render(request, 'main.html')


def loadAllData(request):
    all_data = models.WeatherData.objects.all().values()
    page_count = len(all_data)

    # 前台传来的页数
    page_index = request.GET.get('page')
    # 前台传来的一页显示多少条数据
    page_limit = request.GET.get('limit')
    # 分页器进行分配
    paginator = Paginator(all_data, page_limit)
    # 前端传来页数的数据
    data = paginator.page(page_index)
    # 放在一个列表里
    all_data_info = [x for x in data]
    datas = {"code": 0, "msg": "", "count": page_count, "data": all_data_info}
    return JsonResponse(datas)


def search(request):
    if request.method == 'GET':
        return render(request, 'search.html')


def searchstate(request):
    if request.method == 'GET':
        return render(request, 'searchstate.html')


# xxxxxxxxxxxxxxxxx
def loadSearchStateData(request):
    state_value = request.GET.get('query')
    state_items = models.WeatherData.objects.filter(state=state_value).values()
    page_count = len(state_items)
    # 前台传来的页数
    page_index = request.GET.get('page')
    # 前台传来的一页显示多少条数据
    page_limit = request.GET.get('limit')
    # 分页器进行分配
    paginator = Paginator(state_items, page_limit)
    # 前端传来页数的数据
    data = paginator.page(page_index)
    # 放在一个列表里
    all_data_info = [x for x in data]
    datas = {"code": 0, "msg": "", "count": page_count, "data": all_data_info}
    return JsonResponse(datas)


def loadSearchCityData(request):
    city_value = request.GET.get('query')
    city_items = models.WeatherData.objects.filter(city=city_value).values()
    page_count = len(city_items)
    # 前台传来的页数
    page_index = request.GET.get('page')
    # 前台传来的一页显示多少条数据
    page_limit = request.GET.get('limit')
    # 分页器进行分配
    paginator = Paginator(city_items, page_limit)
    # 前端传来页数的数据
    data = paginator.page(page_index)
    # 放在一个列表里
    all_data_info = [x for x in data]
    datas = {"code": 0, "msg": "", "count": page_count, "data": all_data_info}
    return JsonResponse(datas)


def loadSearchCityStateData(request):
    search = request.GET.get('query')
    args = ()
    if search:
        args = (
            Q(state__icontains=search)
            | Q(city__icontains=search),
        )
    state_items = models.WeatherData.objects.filter(*args).values('weather', 'city').annotate(
        count=Count('weather')).order_by('city')
    page_count = len(state_items)
    # 前台传来的页数
    page_index = request.GET.get('page')
    # 前台传来的一页显示多少条数据
    page_limit = request.GET.get('limit')
    # 分页器进行分配
    paginator = Paginator(state_items, page_limit)
    # 前端传来页数的数据
    data = paginator.page(page_index)
    # 放在一个列表里
    all_data_info = [x for x in data]
    datas = {"code": 0, "msg": "", "count": page_count, "data": all_data_info}
    return JsonResponse(datas)


def loadSearchDtData(request):
    dt_value = request.GET.get('query')
    dt_items = models.WeatherData.objects.filter(dt=dt_value).values()
    page_count = len(dt_items)
    # 前台传来的页数
    page_index = request.GET.get('page')
    # 前台传来的一页显示多少条数据
    page_limit = request.GET.get('limit')
    # 分页器进行分配
    paginator = Paginator(dt_items, page_limit)
    # 前端传来页数的数据
    data = paginator.page(page_index)
    # 放在一个列表里
    all_data_info = [x for x in data]
    datas = {"code": 0, "msg": "", "count": page_count, "data": all_data_info}
    return JsonResponse(datas)


def loadSelectData(request):
    state_datas = models.WeatherData.objects.all().values('state').distinct()
    city_datas = models.WeatherData.objects.all().values('city').distinct()
    dt_datas = models.WeatherData.objects.all().values('dt').distinct()

    # 注意：QuerySet类型无法直接序列化，需要将其转成列表
    dic = {
        'state_datas': list(state_datas),
        'city_datas': list(city_datas),
        'dt_datas': list(dt_datas),
    }
    return JsonResponse(dic)


from django.db.models import Avg, Sum, Max, Min, Count, Q


def max_temp_state(request):
    name = []
    data = []
    name_min = []
    data_min = []
    state_max_temps = models.WeatherData.objects.values('state').annotate(Max('max_temp'))
    state_min_temps = models.WeatherData.objects.values('state').annotate(Min('min_temp'))
    for dic in state_max_temps:
        name.append(dic['state'])
        data.append(dic['max_temp__max'])

    for dic in state_min_temps:
        name_min.append(dic['state'])
        data_min.append(dic['min_temp__min'])
    # return render(request, "max_temp_state.html", {"name": name, "data": data})
    return render(request, "max_temp_state.html", {"name": name, "data": data,
                                                   "name_min": name_min, "data_min": data_min})

def max_ten_city(request):
    city_min = []
    city_max = []
    data_min = []
    data_max = []
    city_min_temps = models.WeatherData.objects.values('city').annotate(Min('min_temp')).order_by('min_temp')
    city_max_temps = models.WeatherData.objects.values('city').annotate(Max('max_temp')).order_by('-max_temp')

    i = 0
    for dic in city_min_temps:
        city_min.append(dic['city'])
        data_min.append(dic['min_temp__min'])
        i = i+1
        if i > 9 : break

    j = 0
    for dic in city_max_temps:
        city_max.append(dic['city'])
        data_max.append(dic['max_temp__max'])
        j = j+1
        if j > 9 : break
    return render(request, "max_ten_city.html", {"city_max": city_max, "data_max": data_max,
                                                 "city_min": city_min, "data_min": data_min})


def chinaMap(request):
    city_max_temps = models.WeatherData.objects.values('city').annotate(Max('max_temp'))
    city_max_temps = list(city_max_temps)
    # print(city_max_temps)
    # 地图的数据必须要求字典的key为name和value
    # 将原始orm请求到的数据中字典的key进行更换（
    # 原始字典：{'city': '北京', 'max_temp__max': '33'}）
    path = "dbzq/city_to_pro.json"
    with open(path, 'r') as f:
        city_to_pro = json.load(f)
    re = []
    re_pros = {}
    t_list_datas = []
    for dic_item in city_max_temps:
        dic = {}
        tmp_re = {}
        dic['name'] = dic_item['city']
        dic['value'] = dic_item['max_temp__max']
        for pro in city_to_pro:
            if dic_item['city'] in city_to_pro[pro]:
                if pro in re_pros:
                    re_pros[pro] = str(max(int(re_pros[pro]), int(dic_item['max_temp__max'])))
                else:
                    re_pros[pro] = dic_item['max_temp__max']

    for key in re_pros:
        dic_tmp = {}
        if '省' in key:
            dic_tmp['name'] = key.replace('省', '')
        elif '市' in key:
            dic_tmp['name'] = key.replace('市', '')
        else:
            dic_tmp['name'] = key
        dic_tmp['value'] = re_pros[key]
        re.append(dic_tmp)
    return render(request, 'chinaMap.html', {'data': re})


def city_temp_state(request):
    city = request.GET.get("city")[0:-1];

    min_temp = []
    max_temp = []
    data = []
    result = models.WeatherData.objects.filter(city=city).values()
    for dic in result:
        min_temp.append(dic['min_temp'])
        max_temp.append(dic['max_temp'])
        data.append(dic['dt'])
    # data[0] = today
    return render(request, "city_temp_state.html",
                  {"data": data, "city": city, "min_temp": min_temp, "max_temp": max_temp})


def password_reset(request):
    if request.method == 'POST':
        try:
            code = request.POST.get('code')
            email = request.POST.get('email')  # 获取前端邮箱
            password = request.POST.get('password')
            user = models.RegistUser.objects.filter(email=email).first()
            if user:
                cache_code = cache.get(email)
                if not code:
                    return JsonResponse({'code': 400, 'msg': '验证码已失效'})
                if code == cache_code:
                    user.password = password
                    user.save()
                    send_mail('密码重置成功',
                              '您的新密码为: %s' % password, 'heyu2021best@163.com',
                              [email], fail_silently=True)
                    # msg = 'unsprint'
                    # return redirect(url_for('login', msg=msg))
                    return redirect('login')
                return render(request, 'password_reset.html', {'msg': '验证码错误, 请检查后重试！'})
            return render(request, 'password_reset.html', {'msg': '邮箱不存在, 请检查后重试！'})
        except:
            return render(request, 'password_reset.html', {'msg': '网络有误！'})
    else:
        return render(request, 'password_reset.html')


def get_verify_code(request):
    email = request.POST.get('email')
    if email:
        code = customize_random_str(4)
        send_mail('密码重置',
                  '您的验证码为: %s' % code, 'heyu2021best@163.com',
                  [email], fail_silently=True)
        cache.set(email, code, timeout=300)
        return JsonResponse({'status': 'success', 'time_remain': 60})  # 'result': result})
    return JsonResponse({'code': 400, 'msg': "邮箱错误"})


def customize_random_str(i: int):
    digits = 'qwertyuiopasdfghjklzxcvbnm0123456789'
    salt = random.SystemRandom()
    random_str = ''.join(salt.sample(digits, k=i))
    return random_str


def logout(request):
    request.session.flush()
    # 2. 重定向到 登录界面
    return redirect('login')


def modPwd(request):
    if request.method == 'GET':
        return render(request, 'modPassword.html')
    else:
        # 表单数据的捕获
        username = request.POST.get('name')
        try:
            user = models.RegistUser.objects.get(username=username)
            password = request.POST.get('password')
            newpassword = request.POST.get('newpassword')
            newrepeatpwd = request.POST.get('newrepeatpwd')

            if (newpassword != newrepeatpwd):
                return render(request, 'modPassword.html', {'msg': '两次密码不一致，请重新输入'})
            elif user.password == password:
                user = models.RegistUser(id=user.id, username=username, password=newpassword, email=user.email,
                                         phone=user.phone)
                user.save()
                return render(request, 'modPassword.html', {'msg': '修改成功'})
            else:
                return render(request, 'modPassword.html', {'msg': '原密码错误，请确认后重新输入'})


        except:
            return render(request, 'modPassword.html', {'msg': '用户不存在'})
