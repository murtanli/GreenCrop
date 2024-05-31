from datetime import datetime
import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Avg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import localtime
from django.views import View

from greenhouse_page.models import *


def auth(request):
    if request.method == 'POST':
        login_text = request.POST.get('login')
        password_text = request.POST.get('password')

        user = authenticate(username=login_text, password=password_text)

        if user is not None:
            login(request, user)
            messages.success(request, 'Авторизация прошла успешно!')

            if Greenhouse.objects.filter(user=user).exists():
                return redirect('profile')
            else:
                return redirect('add_gr_hs')
        else:
            messages.error(request, 'Ошибка авторизации, неправильно введен пароль или логин')
            return redirect('auth_page')
    else:
        return render(request, 'auth.html')


def sign_in(request):
    if request.method == 'POST':
        login_text = request.POST.get('login')
        email_text = request.POST.get('email')
        password_text = request.POST.get('password')
        try:
            user = User.objects.create_user(username=login_text, email=email_text, password=password_text)
            messages.success(request, 'Регистрация прошла успешно!')
        except:
            messages.error(request,'Ошибка регистрации. Пользователь с таким логином уже существует или произошла ошибка при заполнении формы.')

        return redirect('main_page')
    else:
        return redirect('main_page')

def add_gr_hs(request):
    user = request.user
    title = 'Добавить теплицу'
    patch = 'Home / Добавить теплицу'
    context = {'user': user,
               'title': title,
               'patch': patch}
    if user.is_authenticated:
        return render(request, 'add_gr_hs.html', context=context)
    else:
        messages.error(request,'Авторизуйтесь !')
        return redirect('main_page')


def save_gr_hs(request):
    user = request.user
    if request.method == 'POST':
        imei_text = request.POST.get('imei')
        city_text = request.POST.get('city')
        area_text = request.POST.get('area')
        sowing_text = request.POST.get('sowing')
        latitude_text = request.POST.get('latitude')
        longitude_text = request.POST.get('longitude')
        # Список для сбора ошибок
        if sowing_text == 'on':
            sowing_text = True
        else:
            sowing_text = False

        error_list = []

        # Проверка на существование теплицы с таким IMEI
        if Greenhouse.objects.filter(imei=imei_text).exists():
            messages.error(request, 'Данная теплица существует в базе')
            return redirect('add_gr_hs')

        # Проверка на пустые поля
        if not imei_text or len(imei_text) < 10:
            error_list.append('Введите корректный imei!')
        if not city_text:
            error_list.append('Введите город!')
        if not area_text:
            error_list.append('Введите площадь теплицы !')
        if not latitude_text or not longitude_text:
            error_list.append('Выберите местоположение теплицы на карте!')

        # Если есть ошибки, отправляем их пользователю
        if error_list:
            for error in error_list:
                messages.error(request, error)
            return redirect('add_gr_hs')

        # Сохранение теплицы
        try:
            gr_hs = Greenhouse(
                user=user,
                imei=imei_text,
                location=city_text,
                area=area_text,
                latitude=latitude_text,
                longitude=longitude_text,
                sowing=sowing_text,
            )
            gr_hs.save()

            gr_registry = Registry(
                greenhouse=gr_hs,
                datetime=datetime.now(),
                water=0,
                temp1=0,
                temp2=0,
                temp3=0,
                soil_moisture=0,
                air_humidity=0,
                energy_usage=0,
            )
            gr_registry.save()

            gr_control = GreenhouseControl(
                greenhouse=gr_hs,
                ventilation=False,
                window1=False,
                window2=False,
                water_supply=False,
                lights=False
            )
            gr_control.save()

            messages.success(request, 'Теплица успешно добавлена!')
            return redirect('profile')
        except Exception as e:
            messages.error(request, f'Ошибка в сохранении')
            return redirect('add_gr_hs')
    else:
        return redirect('add_gr_hs')

def profile(request):
    user = request.user
    title = 'Профиль'
    patch = 'Home / Профиль'
    if user.is_authenticated:
        return render(request, 'profile.html', {'user': user, 'title': title, 'patch': patch})
    else:
        messages.error(request,'Авторизуйтесь !')
        return redirect('main_page')

def logout_func(request):
    logout(request)
    return redirect('main_page')

@login_required
def all_gr_hs(request):
    user = request.user
    gr_hs = Greenhouse.objects.filter(user=user)
    greenhouses = []
    all_water = 0
    all_energy = 0
    all_alerts_count = 0
    all_area = sum([gr.area for gr in gr_hs])

    for gr in gr_hs:
        gr_hs_reg = Registry.objects.filter(greenhouse=gr).order_by('-datetime')
        if gr_hs_reg.exists():
            latest_reg = gr_hs_reg.first()
            all_water += latest_reg.water
            all_energy += getattr(latest_reg, 'energy_usage', 0)
            avg_temperature = (latest_reg.temp1 + latest_reg.temp2 + latest_reg.temp3) / 3
            controls = GreenhouseControl.objects.get(greenhouse=gr)
            greenhouses.append({'greenhouse_info': gr,
                                'register': latest_reg,
                                'controls': controls,
                                'avg_temperature': avg_temperature})

        all_alerts_count += Alerts_gr.objects.filter(greenhouse=gr).count()

    all_gr = len(gr_hs)
    all_sowing = len([hs for hs in gr_hs if hs.sowing])  # Проверка на True или None

    title = 'Профиль'
    patch = 'Home / Все теплицы'
    context = {
        'greenhouses': greenhouses,
        'all_gr': all_gr,
        'all_sowing': all_sowing,
        'all_water': all_water,
        'all_alerts_count': all_alerts_count,
        'all_energy': all_energy,
        'all_area': all_area,
        'title': title,
        'user': user,
        'patch': patch
    }
    return render(request, 'all_gr_hs.html', context=context)

def map_data(request):
    user = request.user
    gr = Greenhouse.objects.filter(user=user)

    data = {
        'greenhouses': [{'latitude': greenhouse.latitude, 'longitude': greenhouse.longitude} for greenhouse in gr]
    }
    return JsonResponse(data)


def update_control(request):
    if request.method == 'POST':
        greenhouse_id = request.POST.get('greenhouse_id')
        control = request.POST.get('control')
        status = request.POST.get('status') == 'true'

        greenhouse = GreenhouseControl.objects.get(greenhouse=greenhouse_id)
        print(control)
        if control == 'ventilation':
            greenhouse.ventilation = status
        elif control == 'window1':
            greenhouse.window1 = status
        elif control == 'window2':
            greenhouse.window2 = status
        elif control == 'water_supply':
            greenhouse.water_supply = status
        elif control == 'lights':
            greenhouse.lights = status

        greenhouse.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def monitoring_gr_hs(request, greenhouse_id):
    greenhouse = Greenhouse.objects.get(id=greenhouse_id)
    gr_register = Registry.objects.filter(greenhouse=greenhouse).order_by('-datetime')
    controls = GreenhouseControl.objects.get(greenhouse=greenhouse)
    request.session['greenhouse_id'] = greenhouse_id
    if gr_register.exists():
        latest_reg = gr_register.first()
    try:
        all_alerts = sum([gr for gr in Alerts_gr.objects.filter(greenhouse=greenhouse)])
    except:
        all_alerts = 0
    context = {
        'controls': controls,
        'greenhouse': greenhouse,
        'all_alerts':all_alerts,
        'gr_num': greenhouse.id,
        'sowing': greenhouse.sowing,
        'gr_water': latest_reg.water,
        'gr_energy': latest_reg.energy_usage,
        'gr_area': greenhouse.area,
        'latitude': float(greenhouse.latitude),
        'longitude': float(greenhouse.longitude)
    }
    return render(request, 'greenhouse_info.html', context=context)

def graph_view(request):
    tepl_id = request.session.get('greenhouse_id')
    if tepl_id is not None:#avg_temperature = (latest_reg.temp1 + latest_reg.temp2 + latest_reg.temp3) / 3
        registries = Registry.objects.filter(greenhouse=tepl_id)
        data = {

            'datetime': [localtime(r.datetime).strftime("%d %B %H:%M") for r in registries],
            'avg_temperature': [(r.temp1 + r.temp2 + r.temp3)/3 for r in registries],
            'air_humidity': [r.air_humidity for r in registries],
            'water': [r.water for r in registries],
            'energy_usage': [r.energy_usage for r in registries],
            'soil_moisture': [r.soil_moisture for r in registries],
        }
        return JsonResponse(data)
    else:
        data = {
            'none': 'none'
        }
    return JsonResponse(data)





def test(request):
    return render(request, 'test_add_info.html')
class save_db(View, LoginRequiredMixin):
    def get(self, request, greenhouse_id):
        if request.user.is_authenticated:
            user = request.user
            gr = Greenhouse.objects.filter(id=greenhouse_id)
            num = gr.latest('id')
            new_registry = Registry()


            new_registry.greenhouse = num
            new_registry.datetime = datetime.now()
            new_registry.air_humidity = random.randint(0, 100)
            new_registry.water = random.randint(0, 1000)
            new_registry.temp1 = random.randint(0, 40)
            new_registry.temp2 = random.randint(0, 40)
            new_registry.temp3 = random.randint(0, 40)
            new_registry.energy_usage = random.randint(0, 1000)
            new_registry.soil_moisture = random.randint(0, 100)

            new_registry.save()
            data = {
                'heh': {
                    'id': new_registry.id,
                    'datetime': new_registry.datetime.strftime("%d %B %H:%M"),
                    'air_humidity': new_registry.air_humidity,
                    'water': new_registry.water,
                    'temp1': new_registry.temp1,
                    'temp2': new_registry.temp2,
                    'temp3': new_registry.temp3,
                    'energy_usage': new_registry.energy_usage,
                    'soil_moisture': new_registry.soil_moisture,
                }
            }
        else:
            data = {
                'heh': 'none',
            }
        return JsonResponse(data)