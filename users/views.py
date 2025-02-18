from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 
from django.contrib.auth.views import PasswordResetConfirmView

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = 'users/password_reset_confirm.html'