#from django.shortcuts import render
#from django.http import HttpResponse
from models import *

#from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.models import User
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
#from django.contrib.auth.decorators import login_required
#from django.contrib import messages
#from django.core.mail import send_mail
#from sistema.forms import *
#from django.contrib.auth.views import password_reset
from datetime import *
from time import *
from django.core.urlresolvers import reverse
#import re
#from django.core.files import File
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from django.core.exceptions import PermissionDenied
#import datetime
#import mimetypes
from os import path
import math



# Create your views here.
def index(request):
	a = Numeropessoastotal.objects.all()
	ultimo = len(a)
	oi = a[ultimo-1].num_de_pessoas
	return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def home_admin(request):
	numero_pessoas = Numeropessoastotal.objects.all()
	ultimo = len(numero_pessoas)
	ultimo_numero = numero_pessoas[ultimo-1]
	lista_datahora=[]
	for obj in numero_pessoas:
		datahora = Datahora.objects.filter(id = obj.datahora_id)
		horario = str(datahora[0].hora)+":"+str(datahora[0].minutos)
		lista_datahora.append(horario)
	ultimo = len(numero_pessoas)
	#oi = a[ultimo-1].num_de_pessoas
	return render_to_response('Home_admin.html', locals(), context_instance=RequestContext(request))

def historico_admin(request):
	numero_pessoas = Numeropessoastotal.objects.all()
	ultimo = len(numero_pessoas)
	ultimo_numero = numero_pessoas[ultimo-1]
	lista_datahora=[]
	for obj in numero_pessoas:
		datahora = Datahora.objects.filter(id = obj.datahora_id)
		horario = str(datahora[0].dia)+"/"+str(datahora[0].mes)+","+ str(datahora[0].hora)+":"+str(datahora[0].minutos)
		lista_datahora.append(horario)
	ultimo = len(numero_pessoas)
	#oi = a[ultimo-1].num_de_pessoas
	return render_to_response('historico_admin.html', locals(), context_instance=RequestContext(request))

# def visualizar_formulario(request):
#     todos_formularios = Perguntas.objects.all()
#     for form in todos_formularios:
#         todas_respostasform = Respostas.objects.filter(form_correspondente = form)
#         numero_respostas=len(todas_respostasform)
#         form.numero_respostas=numero_respostas
#         form.save()
#     return render_to_response('visualizar_formulario.html', locals(), context_instance=RequestContext(request))