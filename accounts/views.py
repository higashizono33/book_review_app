from django.db import models
from .forms import CustomUserCreateForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin

User = get_user_model()

class IndexView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreateForm
    success_url = reverse_lazy('index')
    template_name = 'registration/index.html'
    success_message = "You are successfully registered! Please login"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['login_form'] = AuthenticationForm
        return context

def login_view(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                print('user is not found')
        else:
            form = CustomUserCreateForm
            context = {
                'form': form,
                'login_form': login_form,
            }
            return render(request, "registration/index.html", context=context)