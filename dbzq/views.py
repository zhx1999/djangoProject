from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from dbzq import models
from django.core.paginator import Paginator
from django.core import serializers
from tools import checkCode
from io import BytesIO

# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
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
                return render(request,'login.html',{'msg':'登录失败，用户名不存在！'})
            if user.password == password:
                return render(request,'main.html')
            else:
                return render(request,'login.html',{'msg':'登录失败，密码错误！'})
        else:
            return render(request, 'login.html', {'msg':'登陆失败，验证码错误！'})

def regist(request):
    if request.method == 'GET':
        return render(request,'regist.html')
    else:
        #表单数据的捕获
        username = request.POST.get('name')
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
                return render(request,'regist.html',{'msg':'注册失败！两次密码不一致......'})
            else:
                user = models.RegistUser(username=username,password=password,email=email,phone=phone)
                user.save()
                return render(request,'registRight.html')

def create_code_img(request):
    f = BytesIO()  # 在内存中临时存放验证码图片

    img, code = checkCode.create_validate_code() # 生成 图片,验证码

    request.session['check_code'] = code  # 将验证码存在服务器的session中，用于校验
    img.save(f, 'PNG')  # 生成的图片放置于开辟的内存中


    return HttpResponse(f.getvalue())  # 将内存的数据读取出来，并以HttpResponse返回

def mainView(request):
    return render(request,'main.html')

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
        return render(request,'search.html')



#xxxxxxxxxxxxxxxxx
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

    #注意：QuerySet类型无法直接序列化，需要将其转成列表
    dic = {
        'state_datas':list(state_datas),
        'city_datas':list(city_datas),
        'dt_datas':list(dt_datas),
    }
    return JsonResponse(dic)

from django.db.models import Avg, Sum, Max, Min, Count
def max_temp_state(request):
    name = []
    data = []
    state_max_temps = models.WeatherData.objects.values('state').annotate(Max('max_temp'))
    for dic in state_max_temps:
        name.append(dic['state'])
        data.append(dic['max_temp__max'])
    return render(request, "max_temp_state.html", {"name": name, "data": data})

def chinaMap(request):
    city_max_temps = models.WeatherData.objects.values('city').annotate(Max('max_temp'))
    city_max_temps = list(city_max_temps)
    print(city_max_temps)
    #地图的数据必须要求字典的key为name和value
    #将原始orm请求到的数据中字典的key进行更换（
    # 原始字典：{'city': '北京', 'max_temp__max': '33'}）
    t_list_datas = []
    for dic_item in city_max_temps:
        dic = {}
        dic['name'] = dic_item['city']
        dic['value'] = dic_item['max_temp__max']
        t_list_datas.append(dic)
    return render(request,'chinaMap.html',{'data':t_list_datas})


