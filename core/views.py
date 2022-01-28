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
        username = form['username'].value()
        password = form['password'].value()
        User.objects.create_user(username=username, password=password)      
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        
        return redirect('prestador_create_view')
    
    def form_invalid(self, form):
        return render(self.request, self.template_name, {'erro': 'Desculpe, email já utilizado'})

@method_decorator(login_required(login_url='login_view'), name='dispatch')
class PrestadorCreateView(CreateView):
    model = Prestador
    template_name = './prestador/criar.html'
    fields = ['nome', 'ramo', 'whatsapp', 'foto_perfil']
    success_url = 'endereco_create_view'

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


@method_decorator(login_required(login_url='login_view'), name='dispatch')
class ServicoCreateView(CreateView):
    model = Servico
    template_name = './servico/criar.html'
    fields = ['nome', 'descricao', 'preco']
    success_url = 'dashboard_view'

    def form_valid(self, form):
        form = form.save(commit=False)
        user = self.request.user
        prestador = Prestador.objects.get(user=user)
        form.prestador = prestador
        form.save()
        return redirect(self.success_url)
@method_decorator(login_required(login_url='login_view'), name='dispatch')
class EnderecoCreateView(CreateView):
    model = Endereco
    template_name = './endereco/criar.html'
    fields = ['rua', 'numero', 'bairro', 'cidade','estado']
    success_url = 'dashboard_view'

    def get(self, request, *args: str, **kwargs):
        queryset = Endereco.objects.all().filter(user=self.request.user)
        if queryset.count() == 1:
            return redirect('dashboard_view')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form = form.save(commit=False)
        form.user = self.request.user
        form.save()
        return redirect(self.success_url)

def endereco_filter(data, cidade):
    users = Endereco.objects.all().filter(cidade__icontains=cidade)
    usuarios = []
    for i in users:
        usuarios.append(i.user)
    data = data.filter(user__in=usuarios)
    return data

def endereco_filter_servico(data, cidade):
    users = Endereco.objects.all().filter(cidade__icontains=cidade)
    usuarios = []
    for i in users:
        usuarios.append(i.user)
    prestadores = Prestador.objects.all().filter(user__in=usuarios)
    data = data.filter(prestador__in=prestadores)
    return data

def filtragem_prestador(prestadores, query):
    nome = query['nome_filter']
    area = query['area_filter']
    if nome != '':
        prestadores = prestadores.filter(nome__icontains=nome)
    if area != '':
        prestadores = prestadores.filter(ramo__icontains=area)
    cidade = query['cidade_filter']
    if cidade != '':
        prestadores = endereco_filter(prestadores, cidade)
    return prestadores

def filtragem_servico(servicos, query):
    nome = query['nome_filter']
    preco = query['preco_filter']
    if nome != '':
        servicos = servicos.filter(nome__icontains=nome)
    if preco != '':
        preco_min = float(preco)*0.8
        preco_max = float(preco)*1.2
        servicos = servicos.filter(preco__lte=preco_max, preco__gte=preco_min)
    cidade = query['cidade_filter']
    if cidade != '':
        servicos = endereco_filter_servico(servicos, cidade)
    return servicos

class PrestadorListView(ListView):
    model = Prestador
    template_name = './prestador/listar.html'
    object_name = 'prestadores'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.dict()
        prestadores = Prestador.objects.all()
        if query:
            prestadores = filtragem_prestador(prestadores, query)            
        context['prestadores'] =  prestadores
        return context

@method_decorator(login_required(login_url='login_view'), name='dispatch')
class ServicoDeleteView(View):
    def get(self,request, pk):
        servico = Servico.objects.filter(id=pk).first()
        if servico.prestador.user == self.request.user:
            servico.delete()
        return redirect('dashboard_view')

class ServicoListView(ListView):
    model = Servico
    template_name = './servico/listar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.dict()
        servicos = Servico.objects.all() 
        if query:
            servicos = filtragem_servico(servicos, query)
        context['servicos'] = servicos
        return context

class ServicoDetailView(DetailView):
    context_object_name = 'Servico'
    queryset = Servico.objects.all()
    template_name = './servico/detalhe.html'

class PrestadorDetailView(DetailView):
    context_object_name = 'prestador'
    queryset = Prestador.objects.all()
    template_name = './prestador/detalhe.html'

@method_decorator(login_required(login_url='login_view'), name='dispatch')
class PrestadorUpdateView(UpdateView):
    model = Prestador
    fields = ['nome', 'ramo', 'whatsapp', 'foto_perfil']
    template_name = './prestador/update.html'
    success_url = reverse_lazy('dashboard_view')

@method_decorator(login_required(login_url='login_view'), name='dispatch')
class ServicoUpdateView(UpdateView):
    model = Servico
    fields = ['nome', 'descricao', 'preco']
    template_name = './servico/atualizar.html'
    success_url = reverse_lazy('dashboard_view')

    def get(self, request, *args: str, **kwargs):
        prestador = Prestador.objects.all().filter(user=self.request.user).first()
        
        if self.get_object().prestador == prestador:
            return super().get(request, *args, **kwargs)
        
        return redirect('dashboard_view')
class EnderecoUpdateView(UpdateView):
    model = Endereco
    fields = ['rua','numero', 'bairro', 'cidade', 'estado']
    template_name = './endereco/update.html'
    success_url = reverse_lazy('dashboard_view')



@method_decorator(login_required(login_url='login_view'), name='dispatch')
class DashboardView(View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        queryset = Prestador.objects.all().filter(user=self.request.user)
        if queryset.count() == 1:
            prestador = queryset.first()
            servicos = Servico.objects.all().filter(prestador=prestador)
            return render(request, self.template_name, {'prestador':prestador, 'servicos':servicos})
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
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_view')

        context = {'erro':'Email ou senha incorretos, tente novamente'}
        return render(request, self.template_name, context)

@method_decorator(login_required(login_url='login_view'), name='dispatch')
class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('index_template_view')

class InicioView(View):
    template_name = './inicial/index.html'

    def get(self, request):
        content = {}
        if self.request.user.is_authenticated:
            content = {'usuario':self.request.user}
        return render(request, self.template_name, content)
