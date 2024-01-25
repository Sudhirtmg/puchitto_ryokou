from django.shortcuts import render,redirect,Http404
from user_app.models import Profile
from user_app.forms import *
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
# Create your views here.

def signup(rq):
    form=RegisterForm()
    if rq.method=='POST':
        form=RegisterForm(rq.POST or None)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(rq,f'{username},登録完了しました')
            return redirect('signin')
    else:
        form=RegisterForm()
    context={
        'form':form
    }
    return render(rq,'User_Auth/signup.html',context)
def signin(rq):
    if rq.user.is_authenticated:
        messages.warning(rq,'ログイン済み')
        return redirect('index')
    else:
        if rq.method=='POST':
            email=rq.POST.get('email')
            password=rq.POST.get('password')
            user=authenticate(rq,email=email,password=password)
            if user is not None:
                login(rq,user)
                messages.success(rq,f'{email},ログインしました。')
                return redirect('index')
            else:
                messages.error(rq,'メールアドレスとパスワードに誤りがあります。もう一度入力し直してください')
                return redirect('signin')            
    return render(rq,'User_Auth/signin.html')

def singout(rq):
    logout(rq)
    messages.success(rq,'ログアウしました')
    return redirect('signin')

def PROFILE_UPDATE(request):
    if request.method == 'POST':
        location = request.POST.get('prefecture')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        try:
            user = User.objects.get(id=user_id)

            # Update only if the field is present in the POST data
            if location:
                user.location = location
            if username:
                user.username = username
            if email:
                user.email = email
            if password:
                user.set_password(password)

            user.save()

            messages.success(request, 'プロファイルをアップデートしました')
            return redirect('dashboard')
        except User.DoesNotExist:
            messages.error(request, 'ユーザが見つかりませんでした。')
    return render(request, 'User_Auth/profile_update.html')