from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import *
from django.contrib import messages
import jdatetime
from django.http import JsonResponse

def index(request):
    return render(request, "index.html",{})

def booking(request):
    #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validWeekday(22)

    #Only show the days that are not full:
    validateWeekdays = isWeekdayValid(weekdays)
    

    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')
        if service == None:
            messages.success(request, "خدمت مورد نظر را انتخاب کنید!")
            return redirect('booking')

        #Store day and service in django session:
        request.session['day'] = day
        request.session['service'] = service

        return redirect('bookingSubmit')


    return render(request, 'booking.html', {
            'weekdays':weekdays,
            'validateWeekdays':validateWeekdays,
        })

def bookingSubmit(request):
    user = request.user
    times = [
        "8 AM", "8:30 AM", "9 AM", "9:30 AM", "10 AM", "10:30 AM", "11 AM", "11:30 AM", "12 AM", "3 PM"
        , "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM"
    ]
    today = datetime.now()
    minDate = jdatetime.datetime.fromgregorian(datetime=today).strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=22)
    strdeltatime = jdatetime.datetime.fromgregorian(datetime=deltatime).strftime('%Y-%m-%d')
    maxDate = strdeltatime
    day = request.session.get('day')

    #Get stored data from django session:
    service = request.session.get('service')

    
    #Only show the time of the day that has not been selected before:
    hour = checkTime(times, day)
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)
        if service != None:
            if day <= maxDate and day >= minDate:
                if date == 'Monday' or date == 'Saturday' or date == 'Wednesday' or date == 'Tuesday' or date == 'Sunday' or date == 'Thursday':
                    if Appointment.objects.filter(day=day).count() < 11:
                        if Appointment.objects.filter(day=day, time=time).count() < 1:
                            AppointmentForm = Appointment.objects.get_or_create(
                                user = user,
                                service = service,
                                day = day,
                                time = time,
                            )
                            messages.success(request, "نوبت ذخیره شد!")
                            return redirect('index')
                        else:
                            messages.success(request, "زمان انتخابی قبلا رزرو شده!")
                    else:
                        messages.success(request, "ظرفیت زمان انتخابی پر میباشد!")
                else:
                    messages.success(request, "تاریخ انتخابی صحیح نیست")
            else:
                    messages.success(request, "زمان انتخابی در دوره تعریف شده نیست!")
        else:
            messages.success(request, "سرویس را انتخاب کنید!")


    return render(request, 'bookingSubmit.html', {
        'times':hour,
    })

def userPanel(request):
    user = request.user
    appointments = Appointment.objects.filter(user=user).order_by('day', 'time')
    return render(request, 'userPanel.html', {
        'user':user,
        'appointments':appointments,
    })

def userUpdate(request, id):
    appointment = Appointment.objects.get(pk=id)
    userdatepicked = appointment.day
    #Copy  booking:
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')

    #24h if statement in template:
    delta24 = (userdatepicked).strftime('%Y-%m-%d') >= (today + timedelta(days=1)).strftime('%Y-%m-%d')
    #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validWeekday(22)

    #Only show the days that are not full:
    validateWeekdays = isWeekdayValid(weekdays)
    

    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')

        #Store day and service in django session:
        request.session['day'] = day
        request.session['service'] = service

        return redirect('userUpdateSubmit', id=id)


    return render(request, 'userUpdate.html', {
            'weekdays':weekdays,
            'validateWeekdays':validateWeekdays,
            'delta24': delta24,
            'id': id,
        })

def userUpdateSubmit(request, id):
    user = request.user
    times = [
        "8 AM", "8:30 AM", "9 AM", "9:30 AM", "10 AM", "10:30 AM", "11 AM", "11:30 AM", "12 AM", "3 PM"
        , "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM"
    ]
    today = datetime.now()
    minDate = jdatetime.datetime.fromgregorian(datetime=today).strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=22)
    strdeltatime = jdatetime.datetime.fromgregorian(datetime=deltatime).strftime('%Y-%m-%d')
    maxDate = strdeltatime
    day = request.session.get('day')

    service = request.session.get('service')
    
    #Only show the time of the day that has not been selected before and the time he is editing:
    hour = checkEditTime(times, day, id)
    appointment = Appointment.objects.get(pk=id)
    userSelectedTime = appointment.time
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if service != None:
            if day <= maxDate and day >= minDate:
                if date == 'Monday' or date == 'Saturday' or date == 'Wednesday':
                    if Appointment.objects.filter(day=day).count() < 11:
                        if Appointment.objects.filter(day=day, time=time).count() < 1 or userSelectedTime == time:
                            AppointmentForm = Appointment.objects.filter(pk=id).update(
                                user = user,
                                service = service,
                                day = day,
                                time = time,
                            ) 
                            messages.success(request, "نوبت ویرایش شد!")
                            return redirect('index')
                        else:
                            messages.success(request, "زمان انتخابی قبلا رزرو شده است!")
                    else:
                        messages.success(request, "ظرفبت روز انتخابی پر است!")
                else:
                    messages.success(request, "تاریخ انتخابی صحیح نیست")
            else:
                    messages.success(request, "زمان انتخابی در دوره کاری نمی باشد!")
        else:
            messages.success(request, "خدمت مورد نظر را انتخاب کنید!")
        return redirect('userPanel')


    return render(request, 'userUpdateSubmit.html', {
        'times':hour,
        'id': id,
    })

def staffPanel(request):

    today = datetime.today()
    minDate = jdatetime.datetime.fromgregorian(datetime=today).strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=10)
    strdeltatime = jdatetime.datetime.fromgregorian(datetime=deltatime).strftime('%Y-%m-%d')
    maxDate = strdeltatime
    #Only show the Appointments 21 days from today
    items = Appointment.objects.filter(day__range=[minDate, maxDate]).order_by('day', 'time')

    return render(request, 'staffPanel.html', {
        'items':items,
    })

def dayToWeekday(x):
    z = datetime.strptime(x, "%Y-%m-%d")
    y = z.strftime('%A')
    return y

def validWeekday(days):
    today = datetime.now()
    weekdays = []
    for i in range(days):
        x = today + timedelta(days=i)
        shamsi_date = jdatetime.datetime.fromgregorian(datetime=x)
        y = shamsi_date.strftime('%A')  # روز هفته به انگلیسی
        if y in  ["Wednesday", "Thursday",  "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]:
            # تبدیل تاریخ میلادی به شمسی
            shamsi_date = jdatetime.datetime.fromgregorian(datetime=x).strftime('%Y-%m-%d')
            weekdays.append(f"{shamsi_date}")
    return weekdays
    
def isWeekdayValid(x):
    validateWeekdays = []
    for j in x:
        if Appointment.objects.filter(day=j).count() < 22:
            validateWeekdays.append(j)
    return validateWeekdays

def checkTime(times, day):
    #Only show the time of the day that has not been selected before:
    x = []
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1:
            x.append(k)
    return x

def checkEditTime(times, day, id):
    #Only show the time of the day that has not been selected before:
    x = []
    appointment = Appointment.objects.get(pk=id)
    time = appointment.time
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1 or time == k:
            x.append(k)
    return x


def test_weekdays(request):
    today = datetime.now()  # دریافت زمان محلی
    weekdays = []

    for i in range(10):  # تست برای 10 روز آینده
        x = today + timedelta(days=i)
        shamsi_date = jdatetime.datetime.fromgregorian(datetime=x)
        y = shamsi_date.strftime('%A')  # روز هفته به فارسی

        if y in ["Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]:
            shamsi_date_str = shamsi_date.strftime('%Y-%m-%d')
            weekdays.append(shamsi_date_str)
        else:
            weekdays.append(y)

    return JsonResponse({'valid_weekdays': weekdays})

def test_weekdays_with_appointments(request):
    weekdays = validWeekday(10)
    validateWeekdays = []

    for j in weekdays:
        count = Appointment.objects.filter(day=j).count()
        validateWeekdays.append({'date': j, 'count': count})

    return JsonResponse({'valid_weekdays': validateWeekdays})