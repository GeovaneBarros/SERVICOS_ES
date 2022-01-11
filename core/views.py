from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from core.forms import *
# Create your views here.

from core.models import *
class SobreTemplateView(TemplateView):
    template_name = './sobre/sobre.html'

class UsuarioCreateView(CreateView):
    model = User
    fields = ['username', 'password']
    template_name = './usuario/criar.html'
    success_url = 'sobre_template_view'

    def form_valid(self, form):
        super().form_valid(form)
        user = form.save(commit=False)
        login(self.request, user)
        return redirect('prestador_create_view')

@method_decorator(login_required(login_url='login_view'), name='dispatch')
class PrestadorCreateView(CreateView):
    model = Prestador
    template_name = './prestador/criar.html'
    fields = ['nome', 'ramo', 'whatsapp', 'foto_perfil']
    success_url = 'dashboard_view'

    def get(self, request, *args: str, **kwargs):
        queryset = Prestador.objects.all().filter(user=self.request.user)
        if queryset.count() == 1:
            return redirect('dashboard_view')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form = form.save(commit=False)
        form.user = self.request.user
        foto_perfil = self.request.FILES.get('id_foto_perfil')
        form.foto_perfil = foto_perfil
        form.save()
        return redirect(self.success_url)

class PrestadorListView(ListView):
    model = Prestador
    template_name = './prestador/listar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prestadores'] = Prestador.objects.all() 
        return context

class PrestadorDetailView(DetailView):
    context_object_name = 'prestador'
    queryset = Prestador.objects.all()
    template_name = './prestador/detalhe.html'

@method_decorator(login_required(login_url='login_view'), name='dispatch')
class PrestadorUpdateView(UpdateView):
    model = Prestador
    fields = ['nome', 'ramo', 'whatsapp', 'foto_perfil']
    template_name = './prestador/update.html'
    success_url = 'dashboard_view'

    def post(self, request, *args: str, **kwargs):
        super().post(request, *args, **kwargs)
        return redirect(self.success_url)

@method_decorator(login_required(login_url='login_view'), name='dispatch')
class DashboardView(View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        queryset = Prestador.objects.all().filter(user=self.request.user)
        if queryset.count() == 1:
            return render(request, self.template_name)
        else:
            return redirect('prestador_create_view')


class LoginView(View):
    template_name = 'login/index.html'

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'dashboard/index.html')
        return render(request, self.template_name)
    
    def post(self, request):
        post = request.POST
        username = post.get('username')
        password = post.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_view')

        context = {'erro':'Email ou senha incorretos'}
        return render(request, self.template_name, context)

@method_decorator(login_required(login_url='login_view'), name='dispatch')
class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('sobre_template_view')
