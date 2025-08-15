from django.shortcuts import render,redirect,get_object_or_404
from defects.models import Defects_details,testers,defect_screen_shorts,developers
from django.contrib.auth.decorators import login_required
from defects.forms import EditDefects,Add_defect
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from defects.utils import send_email_view

# Create your views here.
@login_required(login_url='login')
def alldefects(request):
    data = Defects_details.objects.all()
    total_defects = data.count()
    paginator = Paginator(data,4)
    page_name = request.GET.get('pg')
    data = paginator.get_page(page_name)

    try:
        test = testers.objects.get(tester_name=request.user)
    except testers.DoesNotExist:
        test = None
    return render(request,'defects/alldefects.html',{'data':data,'test':test,'total_defects':total_defects,})



@login_required(login_url='login')
def completed(request):
    data = Defects_details.objects.filter(defect_status='completed')
    defects = Defects_details.objects.filter(assigned_to=request.user)
    total_defects = defects.filter(defect_status="completed").count()
    paginator = Paginator(data,4)
    page_name = request.GET.get('pg')
    data = paginator.get_page(page_name)

    try:
        test = testers.objects.get(tester_name=request.user)
    except testers.DoesNotExist:
        test = None
    context = {
        'data':data,
        'test':test,
        'total_defects':total_defects
    }
    return render(request,'defects/completed.html',context)

@login_required(login_url='login')
def pending(request):
    data = Defects_details.objects.filter(defect_status='not completed')
    defects = Defects_details.objects.filter(assigned_to=request.user)
    total_defects = defects.filter(defect_status="not completed").count()
    paginator = Paginator(data,4)
    page_name = request.GET.get('pg')
    data = paginator.get_page(page_name)

    try:
        test = testers.objects.get(tester_name=request.user)
    except testers.DoesNotExist:
        test = None
    context = {
        'data':data,
        'test':test,
        'total_defects':total_defects
    }
    return render(request,'defects/pending.html',context)


@login_required(login_url='login')
def description(request,id=0):
    des = Defects_details.objects.get(id=id)
    dimg = defect_screen_shorts.objects.filter(defect=des)
    context = {
        'defects':des,
        'defects1':dimg
    }
    return render(request,'defects/description.html',context)

@login_required(login_url='login')
def edit_defects(request,id=0):
    defect = Defects_details.objects.get(id=id)
    if request.method == 'POST':
        form = EditDefects(request.POST,instance=defect)
        if form.is_valid():
            form.save()
            return redirect('alldefects')
    else:
        form = EditDefects(instance=defect)


    return render(request,'defects/edit.html',{'form':form})

 
@login_required(login_url='login')
def add(request):
    if request.method == 'POST':
        form = Add_defect(request.POST)
        if form.is_valid():
            devname = form.cleaned_data['assigned_to']
            print(devname)
            user = User.objects.get(username=devname)
            print(user.email)
            form.save()
            send_email_view(user.email)
            return redirect('alldefects')
    else:
        form = Add_defect()
    return render(request,'defects/add.html',{'form':form})


@login_required(login_url='login')
def delete(request,id):
    try:
        tester = testers.objects.get(tester_name=request.user)
    except tester.DoesNotExist:
        return HttpResponseForbidden('you are not allowed to delete.')
    
    if not tester.is_admin:
        return HttpResponseForbidden('you are not allowed to delete.')
    
    defect = get_object_or_404(Defects_details,id=id)
    defect.delete()
    return redirect('alldefects')



def filter_defect(request):
    dev = developers.objects.all()
    data = Defects_details.objects.all()
    td = len(data)
    tadmin = False
    selected_user = None
    if  request.method == "POST":
        username = request.POST['username']
        selected_user = username
        if username:
            try:
                duser = User.objects.get(username=username)
                developer = developers.objects.get(dev_name=duser)
                data = Defects_details.objects.filter(assigned_to=duser)
                td = len(data)
                try:
                    test = testers.objects.get(tester_name=request.user)
                    if test.is_admin:
                        tadmin=True
                except testers.DoesNotExist:
                    test = None
            except developer.DoesNotExist as e:
                print(e)
    context = {
        'dev':dev,
        'data':data,
        'td':td,
        'tadmin':tadmin,
       'selected_user':selected_user,
    }
    return render(request,'defects/filterdefect.html',context)