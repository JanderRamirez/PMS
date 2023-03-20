from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from account.models import User
import hashlib
# Create your views here.

def welcome(request):
    return render(request, 'login.html') 

def login(request):
    if(request.method == 'POST'):
        try:
            user = User.objects.get(username = request.POST['username'])
            if(user):
                if(user.password == hashlib.md5(request.POST['password'].encode("utf-8")).hexdigest()):
                    request.session['id'] = user.id
                    request.session['image'] = user.profile
                    request.session['name'] = user.f_name + ' ' + user.l_name
                    if(user.type == 1):
                        return JsonResponse({"msg":"staff"})
                    else:
                        return JsonResponse({"msg":"admin"})
                else:
                    return JsonResponse({"msg":"error"})
            else:
                return JsonResponse({"msg":"error"})
        except User.DoesNotExist:
            return JsonResponse({"msg":"error"})
    else:
        return JsonResponse({"msg":"error"})

def logout(request):
    del request.session['name']
    del request.session['id']
    return redirect('/')
