from django.shortcuts import render,redirect
from accounts.forms import UserForm,UserprofileForm,UpdateForm,update_details,ForgotpasswordForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.models import userData
from defects.models import developers,Defects_details
from django.contrib.auth.models import User

# Create your views here.

def registeration(request):
    registered = False
    if request.method == 'POST':
        form = UserForm(request.POST)
        form1 = UserprofileForm(request.POST,request.FILES)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()

            profile = form1.save(commit=False)
            profile.user = user # both model is merged together
            profile.save()
            registered = True
    else:
        form = UserForm()
        form1 = UserprofileForm()
    context={
        'form':form,
        'form1':form1,
        'registered':registered
    }
    
    return render(request,'accounts/registeration.html',context)


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return redirect('home')
            else:
                return HttpResponse('user is not active')
        else:
            return HttpResponse("please check your credentials..!!")
        
    return render(request,"accounts/login.html",{})


@login_required(login_url='login/')
def home(request):
    total_defects = Defects_details.objects.filter(
        assigned_to=request.user
    ).count()

    pending_defects = Defects_details.objects.filter(
        assigned_to=request.user,
        defect_status__iexact="not completed"  # make sure this matches your DB
    ).count()

    context = {
        'total_defects': total_defects,
        'pending_defects': pending_defects,
    }
    return render(request,"accounts/home.html",context)


@login_required(login_url='login/')
def user_logout(request):
    logout(request)
    return redirect('login/')

@login_required(login_url='login/')
def profile(request):
    d=False
    total_defects = 0
    completed = 0
    pending = 0
    try:
        devop = developers.objects.get(dev_name=request.user)
        if devop:
            d=True
            defects = Defects_details.objects.filter(assigned_to=request.user)
            total_defects = defects.count()

            completed = defects.filter(defect_status="completed").count()
            pending = defects.filter(defect_status="not completed").count()
    except developers.DoesNotExist:
        pass
    return render(request,'accounts/profile.html',{'d':d,"total_defects":total_defects,'completed':completed,'pending':pending})



@login_required(login_url='login/')
def update(request):
    if request.method == 'POST':
        form = UpdateForm(request.POST,instance=request.user)
        form1 = update_details(request.POST,request.FILES,instance=request.user.userdata)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            user.save()

            profile = form1.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('profile')
    else:
        form = UpdateForm(instance=request.user)
        form1 = update_details(instance=request.user.userdata)
    return render(request, 'accounts/update.html', {'form': form,'form1':form1})



def forgotpassword(request):
    pasw = False  

    if request.method == 'POST':
        form = ForgotpasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            pasw = True  

    else:
        form = ForgotpasswordForm()

    return render(request, 'accounts/forgotpassword.html', {'form': form, 'pasw': pasw})