from django.shortcuts import render,redirect
from django.views import View
from accounts.forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
class LoginView(View):
    template_name='accounts/login.html'
    def get(self,request):
        user=request.user
        if user.is_authenticated:
            return redirect("/")
        elif user.is_anonymous:
            form=LoginForm()
            return render(request,self.template_name,{'form':form})
    def post(self,request):
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=request.user
            if user.is_anonymous:
                if username in [username.username for username in User.objects.all()]:
                    if User.objects.get(username=username).is_superuser==False:
                        user=authenticate(username=username,password=password)
                        if user and user.is_active==True and user.is_staff:
                            login(request,user)
                            return redirect('/administration')
                        else:
                            context={'login_error':'Username or Password is worng!!','form':form}
                            return render(request,self.template_name,context)
                    elif User.objects.get(username=username).is_superuser==True:
                        context={'login_error':'Username or Password is worng!!','form':form}
                        return render(request,self.template_name,context)
            elif user.is_authenticated:
                return redirect("/")
        else:
            context={'login_error':'Username or Password is worng!!','form':form}
            return render(request,self.template_name,context)
def logout_view(request):
    user=request.user
    if user.is_authenticated:
        logout(request)
        return redirect("accounts:login")
    elif user.is_anonymous:
        return redirect("accounts:login")
