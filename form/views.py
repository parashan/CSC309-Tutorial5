from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from .forms import EnterForm, RegisterForm, LoginForm, ChatForm, ChatModelForm
from django.views.generic.edit import FormView
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from .models import Chat
from datetime import date
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
import json
# from django.forms import EnterForm
# Build a form using Django 3 different ways
# We use templates for our data for now. https://docs.djangoproject.com/en/4.0/intro/tutorial03/

#Note we use shortcut 'render' instead of returning an HttpResponse or TemplateResponse



#Functional 
def form_view(request):
    if request.method == 'POST':

        print(request.POST)

        form = EnterForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('welcome')
        print(form.errors.as_json())
    else:
        form = EnterForm()
    
    return render(request, 'forms/form.html', {'form': form})

# Class Based View

class BasicFormView1(View):
    template_name = 'forms/form.html'
    form_class = EnterForm

    def get(self, request, *args, **kwargs):
        form  = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            return HttpResponseRedirect('/welcome')

        return render(request, self.template_name, {'form': form})


# Class Based FormView

class BasicFormView2(FormView):
    template_name = 'forms/form.html'
    form_class = EnterForm
    success_url = '/welcome'
    
    def form_valid(self, form):

        return super().form_valid(form)
        

# JSON Responses

def sample_json2(request):
    if request.method == 'GET':
        responseData = {
            'id': 1,
            'name': 'Sample 2'
        }
        return HttpResponse(json.dumps(responseData), content_type="application/json")
    return HttpResponse(json.dumps({}), content_type="application/json")

def sample_json(request):
    if request.method == 'GET':
        responseData = {
            'id': 1,
            'name': 'Hans Paras'
        }
        return JsonResponse(responseData)
    return JsonResponse({})



# Authentication
# settings.py contaisn a LOGIN_URL that will be the redirect url
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('signin')



def signin(request):
    if request.user and request.user.is_authenticated:
        return HttpResponseRedirect('/forms/')
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data['user_name']
            password = form.cleaned_data['password']
            user= authenticate(username=user, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/forms/')
            else:
                form.add_error(None, "Incorrect Username or Password")
        return render(request, 'forms/signin.html', {'form': form})

    form = LoginForm()
    return render(request, 'forms/signin.html', {'form': form})

from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':

        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.cleaned_data['user_name']
                password = form.cleaned_data['password1']
                # Can add validation here, but its better to define the validation in Form clean() method
                email = form.cleaned_data['email']
                save_user = User.objects.create_user(user, email=email, password=password)
                save_user.save()
                
                return HttpResponseRedirect('signin')
            except IntegrityError:
                form.add_error(None, "This user already exists")
            except Exception as error:
                print("This error is", error)
                form.add_error(None, "Generic Server Error")            
        

    else:
        form = RegisterForm()
    return render(request, 'forms/register.html', {'form': form})

@login_required
def auth(request):
    return render(request, 'forms/auth.html', {'user': request.user})

@login_required
def chat(request):
    form = ChatForm()
    if request.method == 'POST':
        form=ChatForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            if comment:
                try:
                    user = request.user
                    chat = Chat(user=user, comment=comment, date=date.today())
                    chat.save()
                    form=ChatForm()
                except Exception as error:
                    print("This error is", error)
                    form.add_error(None, "Generic Server Error")     
    
    chats = Chat.objects.all()
    return render(request, 'forms/chat.html', {'chats': chats, 'form': form, 'detail': "form:chat-detail"})
@login_required
def chat_detail(request, slug):
    chat_detail = Chat.objects.get(slug=slug)
    return render(request, 'forms/chat_detail.html', 
        {
            'chat_detail': chat_detail, 
            'chatpage': 'form:chat',  
            'chatupdate':'form:chat-detail-update'
        })
@login_required
def chat_update(request, slug):
    chat_detail = Chat.objects.get(slug=slug)
    if request.method == 'POST':
        form=ChatForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            if comment:
                try:
                    user = request.user
                    chat_detail.comment = comment
                    chat_detail.save()
                    return HttpResponseRedirect(reverse('form:chat-detail', kwargs = {'slug' : chat_detail.slug }))
                except Exception as error:
                    print("This error is", error)
                    form.add_error(None, "Generic Server Error")     
    form = ChatForm({'comment': chat_detail.comment})
    return render(request, 'forms/chat_update_form.html', 
        {
            'form' : form,
            'chat_detail': chat_detail,

        })

class ChatListView(LoginRequiredMixin, ListView):
    model = Chat
    context_object_name='chats'
    template_name="forms/chat.html"

    def get_context_data(self, **kwargs):
        context = super(ChatListView, self).get_context_data(**kwargs)
        context['detail'] = "form:chat-detail2"
        if self.request.method == "POST":
            context['form'] = ChatForm(self.request.POST)
        else:
            context['form'] = ChatForm()
        
        return context

class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Chat
    context_object_name='chat_detail'
    template_name="forms/chat_detail.html"
    def get_context_data(self, **kwargs):
        context = super(ChatDetailView, self).get_context_data(**kwargs)
        context['chatpage'] = "form:chat2"
        context['chatupdate'] = "form:chat-detail-update2"
        
        return context

class ChatUpdateView(LoginRequiredMixin, UpdateView):
    model=Chat
    form_class = ChatModelForm
    context_object_name='chat_detail'
    template_name='forms/chat_update_form.html'
    
    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else: 
            slug="none"
        return reverse('form:chat-detail2', kwargs={'slug': slug})

    def get_context_data(self, **kwargs):
        context = super(ChatUpdateView, self).get_context_data(**kwargs)
        return context



