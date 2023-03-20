from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from account.models import User
from pms_admin.models import Sale, Medicine,Sales_details
import datetime
# Create your views here.

######## INDEX ########

def index(request):
    return render(request, 's_dashboard.html') 

######## PROFILE ########

def profile(request):
    id = request.session['id']
    context = {
        'profile' : User.objects.get(id = id),
    }
    return render(request, 's_profile.html', context)

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
            with open('pms_staff/static/profile/'+file.name, 'wb+') as destination:  
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
            User.objects.filter(id=request.POST['id']).update(password=request.POST['password'])
        if(update):
            return HttpResponse('success')
        else:
            return HttpResponse('fail')

######## SALES ########

def sales(request):
    sales_id = int(Sale.objects.latest('id').id) + 1
    sales = Sales_details.objects.raw('SELECT d.id as id, m.name as name, d.quantity as quantity,d.price as price, ( d.quantity*d.price) as total FROM pms_admin_sales_details as d JOIN pms_admin_medicine as m ON d.med_id = m.id WHERE d.sales_id =' + str(sales_id))
    total = 0
    for sale in sales:
        total+= sale.total
    context = {
        'sales_no'  :       sales_id,
        'meds'      :       Medicine.objects.all(),
        'products'  :       sales,
        'total' : total
    }
    return render(request, 's_sales.html', context)

def get_detail(request, id):
    med = Medicine.objects.get(name=id)
    if(med):
        data = {
            'msg':'success',
            'price': med.s_price,
            'id': med.id,
            }
        return JsonResponse(data)
    else:
        return JsonResponse({'msg':'No data found!'})

def add_sale(request):
    if(request.method == 'POST'):
        med = Sales_details.objects.create(sales_id=request.POST['sales_id'], 
                                    price=request.POST['u_price'],
                                    quantity=request.POST['quantity'],
                                    med_id=request.POST['med_id'],
                                    )
        med.save()
        return JsonResponse({"msg":"success"})
        
    else:
        return JsonResponse({"msg":"error"})

def delete_sale(request, id):
    sales = Sales_details.objects.get(id = id)
    if(sales.delete()):
        return JsonResponse({"msg":"success"})
    else:
        return JsonResponse({"msg":"error"})

def submit_sale(request, id):
    sales = Sales_details.objects.raw("SELECT * FROM pms_admin_sales_details WHERE sales_id = " + str(id))
    for sale in sales:
        qty = Medicine.objects.get(id=sale.med_id)
        Medicine.objects.filter(id=sale.med_id).update(quantity = qty.quantity - sale.quantity)
    Sale.objects.create(staff=request.session['id']).save()
    return JsonResponse({"msg":"success"})

def daily_sales(request):
    # d = datetime.datetime.now().strftime("%Y-%m-%d")

    context = {
        'sales'     :       Sale.objects.raw("SELECT m.id, m.name as name, SUM(d.quantity) as quantity, d.price as price, (d.quantity*d.price) as total FROM pms_admin_sale as s LEFT JOIN pms_admin_sales_details as d ON s.id = d.sales_id LEFT JOIN pms_admin_medicine as m ON d.med_id = m.id GROUP BY d.med_id"),
    }
    return render(request, 'daily.html', context)