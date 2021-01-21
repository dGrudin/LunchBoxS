import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import Type, LunchBox, User, Order, NumberOfLunchBox, OrderComposition, PastOrder, PastOrderComposition, \
    Status
from .form import LunchBoxForm, DelLunchBoxForm, DelUserForm, SignUpForm, ReadyOrderForm, SearchOrderForm, StatusBusy
from .form import TypeUserForm, NumberOfLunchBoxForm, TypeForm


def index(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password1'),
        )
        if user is not None:
            if user.is_active:
                login(request, user)
                lev = Type.objects.get(user=user)
                if (lev.level == 1):
                    return redirect('employee')
                if (lev.level == 2):
                    return redirect('administrator')
            else:
                print("The password is valid, but the account has been disabled!")
        else:
            print("The username and password were incorrect.")

    return render(request, 'index.html')


def LogoutProfile(request):
    logout(request)

    return redirect('index')


def administrator(request):
    userP = get_object_or_404(User, username=request.user.username)
    users = User.objects.filter(type__level__gt=0).exclude(username=request.user.username)
    lbs = LunchBox.objects.all()
    deleteLb = DelLunchBoxForm()
    deleteEmpl = DelUserForm()
    redaction_number = NumberOfLunchBoxForm()
    if request.method == 'POST':
        redaction_number = NumberOfLunchBoxForm(request.POST)
        deleteLb = DelLunchBoxForm(request.POST)
        deleteEmpl = DelUserForm(request.POST)

        if deleteEmpl.is_valid():
            del_id = deleteEmpl.cleaned_data['id_user']
            User.objects.filter(id=del_id).delete()
            return redirect('administrator')
        else:
            deleteEmpl = DelUserForm()

        if deleteLb.is_valid():
            del_id = deleteLb.cleaned_data['del_lunchbox']
            LunchBox.objects.filter(id=del_id).delete()
            return redirect('administrator')
        else:
            deleteLb = DelLunchBoxForm()

        if redaction_number.is_valid():
            lunchbox = LunchBox.objects.get(id=redaction_number.cleaned_data['id_lunchbox'])
            num = redaction_number.cleaned_data['number']
            lunchbox_num = NumberOfLunchBox()
            try:
                lunchbox_num = NumberOfLunchBox.objects.get(lunchbox=lunchbox)
            except ObjectDoesNotExist:
                lunchbox_num = None

            if lunchbox_num != None:
                lunchbox_num = NumberOfLunchBox.objects.get(lunchbox=lunchbox)
                lunchbox_num.number = num
                lunchbox_num.save()
                return redirect('administrator')
            else:
                new_lb_num = NumberOfLunchBox.objects.create(lunchbox=lunchbox, number=num)
                new_lb_num.save()
        else:
            form = LunchBoxForm()

    return render(request, 'admin.html', {'lbs': lbs, 'users': users, 'userP': userP})


def EmplCreate(request):
    user_add = SignUpForm()
    if request.method == 'POST':
        user_add = SignUpForm(request.POST)
        if user_add.is_valid():
            z = user_add.save(commit=False)
            z.save()
            return HttpResponseRedirect(reverse('typeCreate', args=(z.id,)))
        else:
            user_add = SignUpForm()

    return render(request, 'create_eml.html')


def TypeCreate(request, empl_id):
    empl = get_object_or_404(User, id=empl_id)
    create_type = TypeForm()
    if request.method == 'POST':
        create_type = TypeForm(request.POST)
        if create_type.is_valid():
            t = Type.objects.get(user=empl)
            t.level = create_type.cleaned_data['level']
            t.save()
            return redirect('administrator')
        else:
            form = TypeForm()

    return render(request, 'create_type.html')


def employee(request):
    status = get_object_or_404(Status, name="busy")
    st = 0
    if status.st == False:
        st = 0
    else:
        st = 1
    userP = get_object_or_404(User, username=request.user.username)
    orders = Order.objects.all()
    readyOrder = ReadyOrderForm()
    searchOrder = SearchOrderForm()
    stform = StatusBusy()
    if request.method == 'POST':
        readyOrder = ReadyOrderForm(request.POST)
        searchOrder = SearchOrderForm(request.POST)
        stform = StatusBusy(request.POST)
        if stform.is_valid():
            s = stform.cleaned_data['id_status']
            p = False
            if s == 0:
                p = False
            else:
                p = True
            status.st = p
            status.save()
            return redirect('employee')
        else:
            stform = StatusBusy()
        if readyOrder.is_valid():
            id = readyOrder.cleaned_data['id_ready']
            return HttpResponseRedirect(reverse('order', args=(id,)))
        else:
            readyOrder = ReadyOrderForm()
        if searchOrder.is_valid():
            id = searchOrder.cleaned_data['id_search']
            try:
                o = Order.objects.get(id=id)
            except ObjectDoesNotExist:
                o = None

            if o == None:
                return redirect('employee')
            return HttpResponseRedirect(reverse('order', args=(id,)))
        else:
            searchOrder = ReadyOrderForm()
    return render(request, 'employee.html', {'userP': userP, 'orders': orders, 'st': st})


def employee_orders(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        return render(request, 'prepare.html', {'orders': orders})


def LunchRedaction(request, lunch_id):
    lb = get_object_or_404(LunchBox, id=lunch_id)
    redaction_lb = LunchBoxForm()
    if request.method == 'POST':
        redaction_lb = LunchBoxForm(request.POST, request.FILES)
        if redaction_lb.is_valid():
            lb.title = redaction_lb.cleaned_data['title']
            lb.img = redaction_lb.cleaned_data['img']
            lb.description = redaction_lb.cleaned_data['description']
            lb.price = redaction_lb.cleaned_data['price']
            lb.addition = redaction_lb.cleaned_data['addition']
            lb.save()
            return redirect('administrator')
        else:
            form = LunchBoxForm()

    return render(request, 'redaction_lunch.html', {'lb': lb})


def LunchCreate(request):
    create_lb = LunchBoxForm()
    if request.method == 'POST':
        create_lb = LunchBoxForm(request.POST, request.FILES)
        if create_lb.is_valid():
            p = create_lb.save(commit=False)
            p.save()
            return redirect('administrator')
        else:
            form = LunchBoxForm()

    return render(request, 'create_lunch.html')


def OrderV(request, order_id):
    order = Order.objects.get(id=order_id)
    username = request.user.username
    readyOrder = ReadyOrderForm()
    if request.method == 'POST':
        readyOrder = ReadyOrderForm(request.POST)
        if readyOrder.is_valid():
            order = Order.objects.get(id=readyOrder.cleaned_data['id_ready'])
            ordercomposition = OrderComposition.objects.filter(order=order)
            z = PastOrder.objects.create(client=order.client, date=order.date, price=order.price,
                                         employee=username)
            z.save()
            for i in ordercomposition:
                p = PastOrderComposition.objects.create(order=z, lunchbox=i.lunchbox, number=i.number)
                p.save()

            order.delete()
            return redirect('employee')
        else:
            readyOrder = ReadyOrderForm()
    return render(request, 'order.html', {'order': order,'username': username})


def statistics(request):
    userP = get_object_or_404(User, username=request.user.username)

    return render(request, 'statistics.html', {'userP': userP})


def list_employee_add(name, list):
    for i in list:
        if i[0] == name:
            p = i[1] + 1
            i[1] = p
    return list


def statistics_employee(request):
    employee = User.objects.filter(type__level=1)
    order = PastOrder.objects.all()
    list_employee = list()
    for i in employee:
        list_employee.append([i.username, 0])
    for i in order:
        list_employee_add(i.employee, list_employee)
    return render(request, 'statistics_employee.html', {'list_employee': list_employee})

def statistics_employee_graf(request):
    if request.method == 'GET':
        employee_name = request.GET.get('employee_name')
        day_start = request.GET.get('day_start')
        day_end = request.GET.get('day_end')
        month_start = request.GET.get('month_start')
        month_end = request.GET.get('month_end')
        year_start = request.GET.get('year_start')
        year_end = request.GET.get('year_end')
        start_date = datetime.date(int(year_start), int(month_start), int(day_start))
        end_date = datetime.date(int(year_end), int(month_end), int(day_end))
        order_period = PastOrder.objects.filter(date__range=(start_date, end_date), employee=employee_name).order_by("date")
        list_order = list()
        for i in order_period:
            d = i.date.day
            y = i.date.year
            m = i.date.month
            if (proverka_y_m_d(d, y, m, list_order) == True):
                list_order = add_y_m_d(d, y, m, list_order, i.price)
            else:
                list_order.append([y, m, d, 1, i.price])
        return render(request, 'employee/graf.html', {'list_order': list_order})


def statistics_sales(request):
    return render(request, 'statistics_sales.html')


def sales_content(request):
    return render(request, 'sales/sales_content_graf.html')


def sales_content_day(request):
    return render(request, 'sales/sales_content_graf_day.html')


def proverka_y_m(y, m, order):
    for i in order:
        if i[0] == y:
            if i[1] == m:
                return True
    return False


def add_y_m(y, m, order, price):
    for i in order:
        if i[0] == y:
            if i[1] == m:
                z = i[2] + 1
                i[2] = z
                z1 = i[3] + price
                i[3] = z1
    return order


def lunch_y_m(y, m, lunch, composition):
    for i in lunch:
        if i[0] == y:
            if i[1] == m:
                for j in composition:
                    p = i[2] + j.number
                    i[2] = p
    return lunch


def sales_graf_month(request):
    if request.method == 'GET':
        month_start = request.GET.get('month_start')
        month_end = request.GET.get('month_end')
        year_start = request.GET.get('year_start')
        year_end = request.GET.get('year_end')
        order_period = PastOrder.objects.filter(date__month__range=(month_start, month_end),
                                                date__year__range=(year_start, year_end)).order_by("date")
        list_order = list()
        list_lunchbox = list()
        for i in order_period:
            y = i.date.year
            m = i.date.month
            if (proverka_y_m(y, m, list_order) == True):
                list_order = add_y_m(y, m, list_order, i.price)
            else:
                list_order.append([y, m, 1, i.price])
            composition = PastOrderComposition.objects.filter(order=i)
            if(proverka_y_m(y, m, list_lunchbox) == False):
                list_lunchbox.append([y, m, 0])
            list_lunchbox = lunch_y_m(y, m, list_lunchbox, composition)

    return render(request, 'sales/graf_mounth.html', {'list_order': list_order, 'list_lunchbox': list_lunchbox})

def proverka_y_m_d(d, y, m, order):
    for i in order:
        if i[0] == y:
            if i[1] == m:
                if i[2] == d:
                    return True
    return False


def add_y_m_d(d, y, m, order, price):
    for i in order:
        if i[0] == y:
            if i[1] == m:
                if i[2] == d:
                    z = i[3] + 1
                    i[3] = z
                    z1 = i[4] + price
                    i[4] = z1
    return order


def lunch_y_m_d(d, y, m, lunch, composition):
    for i in lunch:
        if i[0] == y:
            if i[1] == m:
                if i[2] == d:
                    for j in composition:
                        p = i[3] + j.number
                        i[3] = p
    return lunch

def sales_graf_day(request):
    if request.method == 'GET':
        day_start = request.GET.get('day_start')
        day_end = request.GET.get('day_end')
        month_start = request.GET.get('month_start')
        month_end = request.GET.get('month_end')
        year_start = request.GET.get('year_start')
        year_end = request.GET.get('year_end')
        start_date = datetime.date(int(year_start), int(month_start), int(day_start))
        end_date = datetime.date(int(year_end), int(month_end), int(day_end))
        order_period = PastOrder.objects.filter(date__range=(start_date, end_date)).order_by("date")
        list_order = list()
        list_lunchbox = list()
        for i in order_period:
            d = i.date.day
            y = i.date.year
            m = i.date.month
            if (proverka_y_m_d(d, y, m, list_order) == True):
                list_order = add_y_m_d(d, y, m, list_order, i.price)
            else:
                list_order.append([y, m, d, 1, i.price])
            composition = PastOrderComposition.objects.filter(order=i)
            if(proverka_y_m_d(d, y, m, list_lunchbox) == False):
                list_lunchbox.append([y, m, d, 0])
            list_lunchbox = lunch_y_m_d(d, y, m, list_lunchbox, composition)

    return render(request, 'sales/graf_day.html', {'list_order': list_order, 'list_lunchbox': list_lunchbox})

def lunch_all_add(t, n, list):
    for i in list:
        if i[0] == t:
            p = i[1] + n
            i[1] = p
    return list

def statistics_lunchboxs(request):
    lunchboxs = LunchBox.objects.all()
    composition = PastOrderComposition.objects.all()
    list_lunchboxs = list()
    for i in lunchboxs:
        list_lunchboxs.append([i.title, 0])
    for i in composition:
        title = i.lunchbox.title
        number = i.number
        list_lunchboxs = lunch_all_add(title, number,list_lunchboxs)
    return render(request, 'statistics_lunchboxs.html', {'list_lunchboxs': list_lunchboxs})


def lunchbox_graf(request):
    if request.method == 'GET':
        day_start = request.GET.get('day_start')
        day_end = request.GET.get('day_end')
        month_start = request.GET.get('month_start')
        month_end = request.GET.get('month_end')
        year_start = request.GET.get('year_start')
        year_end = request.GET.get('year_end')
        start_date = datetime.date(int(year_start), int(month_start), int(day_start))
        end_date = datetime.date(int(year_end), int(month_end), int(day_end))
        order_period = PastOrder.objects.filter(date__range=(start_date, end_date)).order_by("date")
        list_lunchboxs = list()
        lunchboxs = LunchBox.objects.all()
        for i in lunchboxs:
            list_lunchboxs.append([i.title, 0])
        for i in order_period:
            composition = PastOrderComposition.objects.filter(order=i)
            for i in composition:
                title = i.lunchbox.title
                number = i.number
                list_lunchboxs = lunch_all_add(title, number, list_lunchboxs)

    return render(request, 'lunchbox/graf.html', {'list_lunchbox': list_lunchboxs, 'start_date': start_date, 'end_date': end_date})
