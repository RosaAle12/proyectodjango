from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.conf import settings


def login_view(request):
    template_view = "auth-login-basic.html"  # Asegúrate de que este sea el nombre correcto de tu template de login
    
    if request.method == 'POST':
        username = request.POST.get('email-username')  # Asegúrate de que este nombre coincide con el campo del formulario
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('index')  # Redirige a 'index' después de iniciar sesión
            else:
                messages.error(request, '⚠️Usuario inactivo, verifica tu correo para activar la cuenta⚠️')
        else:
            try:
                existing_user = User.objects.get(username=username)
                if existing_user.is_active:
                    messages.error(request, 'Usuario o contraseña inválidos ⚠️')
                else:
                    messages.error(request, 'Usuario inactivo, verifica tu correo para activar la cuenta ⚠️')
            except User.DoesNotExist:
                messages.error(request, 'Usuario o contraseña inválidos ⚠️')
                
        return render(request, template_view)  # Muestra el formulario de login nuevamente con los mensajes de error
    
    return render(request, template_view)

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('auth-login-basic')  # Redirige al login después del logout


def recuperar_view(request):
    template_name = "auth-forgot-password-basic.html"
    
    return render(request,template_name)



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

def recuperar_view(request):
    template_name = "auth-forgot-password-basic.html"
    return render(request, template_name)

def registro_view(request):
    template_view = "auth-register-basic.html"  # Asegúrate de que este sea el nombre correcto del archivo de plantilla
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Validar que las contraseñas coincidan
        if password1 != password2:
            messages.error(request, '⚠️ Las contraseñas no coinciden ⚠️')
            return redirect('auth-register-basic')  # Redirigir a la vista de registro

        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, '⚠️ El usuario ya existe ⚠️')
            return redirect('auth-register-basic')  # Redirigir a la vista de registro

        # Verificar si el correo ya está registrado
        if User.objects.filter(email=email).exists():
            messages.error(request, '⚠️ El correo electrónico ya está registrado ⚠️')
            return redirect('auth-register-basic')  # Redirigir a la vista de registro

        # Crear usuario inactivo
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.is_active = False  # Marcar usuario como inactivo
        user.save()

        messages.success(request, 'Registro exitoso. Verifica tu correo para activar la cuenta.')
        return redirect('auth-register-basic')  # Redirigir a la vista de registro

    return render(request, template_view)



def logout_view(request):
    logout(request)
    return redirect('auth-login-basic')

