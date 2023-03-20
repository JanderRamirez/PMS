from django.shortcuts import render
from pms_admin.models  import Medicine, Category, Sale, Sales_details
from account.models import User
from django.db import connection
from django.http import HttpResponse, JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
import os

import hashlib
# Create your views here.


######## DASHBOARD ########

def index(request):
    context = {
        'med_count'     :   Medicine.objects.count(),
        'cas_count'     :   User.objects.count(),
        'sales'         :   Sale.objects.raw('SELECT MONTH(s.date) as month, SUM(d.quantity*d.price) as total FROM pms_admin_sale AS s INNER JOIN  pms_admin_sales_details AS d ON s.id = d.sales_id')   
    }
    return render(request, 'dashboard.html', context) 

######## MEDICINE ########

def medicine(request):
    context = {
        'medicines'     : Medicine.objects.raw('SELECT m.*, c.category as cat FROM pms_admin_medicine AS m INNER JOIN  pms_admin_category AS c ON m.category = c.id'),
        'categories'    : Category.objects.all(),
    }
    return render(request, 'medicine.html', context) 

def add_med(request):
    if(request.method == 'POST'):
        if(not Medicine.objects.filter(code=request.POST['code']).exists()):
            med = Medicine.objects.create(code=request.POST['code'], 
                                        category=request.POST['category'], 
                                        name=request.POST['name'], 
                                        description=request.POST['description'],
                                        gen_name=request.POST['gen_name'] , 
                                        p_price=request.POST['p_price'], 
                                        s_price=request.POST['s_price'],
                                        quantity=request.POST['quantity'],
                                        unit=request.POST['unit'],
                                        )
            med.save()
            return JsonResponse({"msg":"success"})
        else:
            return JsonResponse({"msg":"exist"})
    else:
        return JsonResponse({"msg":"error"})

def edit_med(request):
    if(request.method == 'POST'):
        med = Medicine.objects.filter(code=request.POST['code']).update(
                                        category=request.POST['category'], 
                                        name=request.POST['name'], 
                                        description=request.POST['description'],
                                        gen_name=request.POST['gen_name'] , 
                                        p_price=request.POST['p_price'], 
                                        s_price=request.POST['s_price'],
                                        quantity=request.POST['quantity'],
                                        unit=request.POST['unit'],
                                        )
        return JsonResponse({"msg":"success"})

def get_med(request, id):
    med = Medicine.objects.get(id=id)
    data = {
        "id"            : med.id,
        "code"          :med.code,
        "name"          : med.name,
        "description"   : med.description,
        "category"      : med.category,
        "gen_name"      : med.gen_name,
        "p_price"       : med.p_price,
        "s_price"       : med.s_price,
        "quantity"      : med.quantity,
        "unit"          : med.unit,

    }
    return JsonResponse(data)

def add_stock(request):
    if(request.method == 'POST'):
        Medicine.objects.filter(code=request.POST['code']).update(
                                        quantity= (int(request.POST['quantity']) + int(request.POST['added']))
                                        )
        return JsonResponse({"msg":"success"})

######## CATEGORY ########

def category(request):
    context = {
        'categories': Category.objects.all(),
        }
    return render(request, 'category.html', context) 

def add_cat(request):
    if(request.method == 'POST'):
        if(not Category.objects.filter(category=request.POST['category']).exists()):
            cat = Category.objects.create(category=request.POST['category'])
            cat.save()
            return JsonResponse({"msg":"success"})
        else:
            return JsonResponse({"msg":"exist"})
    else:
        return JsonResponse({"msg":"error"})

def get_cat(request, id):
    cat = Category.objects.get(id=id)
    data = {
        "id"            : cat.id,
        "category"      : cat.category,
    }
    return JsonResponse(data)

def edit_cat(request):
    if(request.method == 'POST'):
        Category.objects.filter(id=request.POST['id']).update(category=request.POST['category'])
        return JsonResponse({"msg":"success"})


######## CASHIER ########

def cashier(request):
    context = {
        'cashiers': User.objects.filter(type=1),
        }
    return render(request, 'cashier.html', context) 

def add_cas(request):
    if(request.method == 'POST'):
        cas = User.objects.create(username=request.POST['username'],
                                    password=hashlib.md5(request.POST['password'].encode("utf-8")).hexdigest(),
                                    email=request.POST['email'],
                                    f_name=request.POST['f_name'],
                                    m_name=request.POST['m_name'],
                                    l_name=request.POST['l_name'],
                                    phone=request.POST['phone'],
                                    status=1,
                                    type = 1
                                    )
        cas.save()
        return JsonResponse({"msg":"success"})
    else:
        return JsonResponse({"msg":"error"})

def get_cas(request, id):
    cas = User.objects.get(id=id)
    data = {
        "id"          : cas.id,
        "f_name"      : cas.f_name,
        "m_name"      : cas.m_name,
        "l_name"      : cas.l_name,
        "phone"       : cas.phone,
        "email"       : cas.email,
        "username"    : cas.username,
        "status"      : cas.status
    }
    return JsonResponse(data)

def edit_cas(request):
    if(request.method == 'POST'):
        User.objects.filter(id=request.POST['id']).update(username=request.POST['username'],
                                    email=request.POST['email'],
                                    f_name=request.POST['f_name'],
                                    m_name=request.POST['m_name'],
                                    l_name=request.POST['l_name'],
                                    phone=request.POST['phone'],
                                    status = request.POST['status'])
        if(request.POST['password']):
            User.objects.filter(id=request.POST['id']).update(password=hashlib.md5(request.POST['password'].encode("utf-8")).hexdigest())
        return JsonResponse({"msg":"success"})

######## SALES ########

def sales(request):
    context = {
        'sales'     :       Sale.objects.raw('SELECT s.id as id, s.date as date, c.f_name as fname, c.l_name as lname, sum(d.quantity*d.price) as total FROM pms_admin_sale as s LEFT JOIN pms_admin_sales_details as d ON s.id = d.sales_id JOIN account_user as c ON s.staff = c.id GROUP BY s.id'),
        'monthly'   :       Sale.objects.raw('SELECT s.id as id, MONTH(s.date) as date, sum(d.quantity*d.price) as total FROM pms_admin_sale as s LEFT JOIN pms_admin_sales_details as d ON s.id = d.sales_id JOIN account_user as c ON s.staff = c.id WHERE YEAR(s.date) = YEAR(NOW()) GROUP BY  MONTH(s.date)')
    }
    return render(request, 'sales.html', context)

def get_monthly(request):
        monthly  =     Sale.objects.raw('SELECT s.id as id, MONTH(s.date) as date, sum(d.quantity*d.price) as total FROM pms_admin_sale as s LEFT JOIN pms_admin_sales_details as d ON s.id = d.sales_id JOIN account_user as c ON s.staff = c.id WHERE YEAR(s.date) = YEAR(NOW()) GROUP BY  MONTH(s.date)')
        d = []
        for item in monthly:
            d.append({
                'month' : item.date,
                'total' : item.total,
            })
        data = {
        "sales"         : d
    }
        return JsonResponse(data)

def get_bymed(request):
        bymed  =     Sale.objects.raw('SELECT s.id as id, m.name, sum(d.quantity*d.price) as total FROM pms_admin_sale as s LEFT JOIN pms_admin_sales_details as d ON s.id = d.sales_id JOIN pms_admin_medicine as m ON d.med_id = m.id GROUP BY  m.name')
        d = []
        for item in bymed:
            d.append({
                'name' : item.name,
                'total' : item.total,
            })
        data = {
        "sales"         : d
    }
        return JsonResponse(data)

def get_sales(request, id):
    sales = Sale.objects.get(id=id)
    d = []
    details = Sales_details.objects.raw("SELECT d.id, m.name as name, d.quantity as quantity, d.price as price FROM pms_admin_sales_details as d LEFT JOIN pms_admin_medicine as m ON d.med_id = m.id WHERE d.sales_id = " + str(id))
    for item in details:
        d.append({
            'name' : item.name,
            'quantity' : item.quantity,
            'price' : item.price,
        })
    data = {
        "id"            : sales.id,
        "date"          : sales.date,
        "sales"         : d
    }
    return JsonResponse(data)

def profile(request):
    id = request.session['id']
    context = {
        'profile' : User.objects.get(id = id),
    }
    return render(request, 'profile.html', context)

def update_profile(request):
    if(request.method == 'POST'):
        if(request.FILES['image']):
            file = request.FILES['image']
            update = User.objects.filter(id=request.POST['id']).update(username=request.POST['username'], 
                                                            f_name=request.POST['f_name'], 
                                                            m_name=request.POST['m_name'], 
                                                            l_name=request.POST['l_name'],
                                                            phone=request.POST['phone'] , 
                                                            email=request.POST['email'],
                                                            profile = file.name)
            with open('pms_admin/static/profile/'+file.name, 'wb+') as destination:  
                for chunk in file.chunks():  
                    destination.write(chunk)
            request.session['image'] = file.name
        else:
            update = User.objects.filter(id=request.POST['id']).update(username=request.POST['username'], 
                                                            f_name=request.POST['f_name'], 
                                                            m_name=request.POST['m_name'], 
                                                            l_name=request.POST['l_name'],
                                                            phone=request.POST['phone'] , 
                                                            email=request.POST['email'])
        if(request.POST['password']):
            User.objects.filter(id=request.POST['id']).update(password=hashlib.md5(request.POST['password'].encode("utf-8")).hexdigest())
        if(update):
            return HttpResponse('success')
        else:
            return HttpResponse('fail')