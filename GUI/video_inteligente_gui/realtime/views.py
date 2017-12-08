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
	lotacao = oi/0.8
	datahora = Datahora.objects.all()
	ult = len(datahora)-1
	horario = str(datahora[ult].dia)+"/"+str(datahora[ult].mes)+","+ str(datahora[ult].hora)+":"+str(datahora[ult].minutos)


	numero_fila = 0
	local_fila = Local.objects.filter(tipo = "fila")
	tempo = 0
	lista_pessoas_ids = []
	lista_pessoas_ids_rest = []
	for local in local_fila:
		local_xmax = local.x + local.width
		local_ymax = local.y + local.height
		posicoes_no_local = Posicao.objects.filter(x__gte = local.x , x__lte = local_xmax, y__gte = local.y, y__lte = local_ymax, atual = 1)
		numero_fila +=len(posicoes_no_local)
	for local in local_fila:
		local_xmax = local.x + local.width
		local_ymax = local.y + local.height
		posicoes_no_local_total = Posicao.objects.filter(x__gte = local.x , x__lte = local_xmax, y__gte = local.y, y__lte = local_ymax, atual = 0)
		for posicao_total in posicoes_no_local_total:
			tempo += (posicao_total.instante_final - posicao_total.instante_inicial)
			lista_pessoas_ids.append(posicao_total.pessoa_id)
	total_pessoas_fila = len(set(lista_pessoas_ids))
	tempo_medio = int((tempo/total_pessoas_fila)/100)
	return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def home_admin(request):
	numero_pessoas = Numeropessoastotal.objects.all()
	ultimo = len(numero_pessoas)
	ultimo_numero = numero_pessoas[ultimo-1]
	lista_datahora=[]
	lotacao = ((ultimo_numero.num_de_pessoas)/0.8)
	for obj in numero_pessoas:
		datahora = Datahora.objects.filter(id = obj.datahora_id)
		horario = float(str(datahora[0].hora)+"."+str((datahora[0].minutos)).zfill(2)+str(datahora[0].segundos).zfill(2)+str(datahora[0].milissegundos).zfill(2))
		lista_datahora.append([horario, obj.num_de_pessoas])
		#num_pessoas_total+=obj.num_de_pessoas
	ultimo = len(numero_pessoas)
	numero_fila = 0
	local_fila = Local.objects.filter(tipo = "fila")
	tempo = 0
	lista_pessoas_ids = []
	lista_pessoas_ids_rest = []
	for local in local_fila:
		local_xmax = local.x + local.width
		local_ymax = local.y + local.height
		posicoes_no_local = Posicao.objects.filter(x__gte = local.x , x__lte = local_xmax, y__gte = local.y, y__lte = local_ymax, atual = 1)
		numero_fila +=len(posicoes_no_local)
	for local in local_fila:
		local_xmax = local.x + local.width
		local_ymax = local.y + local.height
		posicoes_no_local_total = Posicao.objects.filter(x__gte = local.x , x__lte = local_xmax, y__gte = local.y, y__lte = local_ymax, atual = 0)
		for posicao_total in posicoes_no_local_total:
			tempo += (posicao_total.instante_final - posicao_total.instante_inicial)
			lista_pessoas_ids.append(posicao_total.pessoa_id)
	total_pessoas_fila = len(set(lista_pessoas_ids))
	tempo_medio = int((tempo/total_pessoas_fila)/100)
	tempo_rest = 0
	posicoes_rest = Posicao.objects.filter(atual = 0)
	for posicao_total_rest in posicoes_rest:
			tempo_rest += (posicao_total_rest.instante_final - posicao_total_rest.instante_inicial)
			lista_pessoas_ids_rest.append(posicao_total_rest.pessoa_id)
	total_pessoas_rest = len(set(lista_pessoas_ids_rest))
	tempo_medio_rest = int((tempo_rest/total_pessoas_rest)/100)








	#oi = a[ultimo-1].num_de_pessoas
	return render_to_response('Home_admin.html', locals(), context_instance=RequestContext(request))

def historico_admin(request):
	numero_pessoas = Numeropessoastotal.objects.all()
	ultimo = len(numero_pessoas)
	ultimo_numero = numero_pessoas[ultimo-1]
	#ultimo_numero.num_de_pessoas
	lotacao = ((ultimo_numero.num_de_pessoas)/0.8)
	lista_datahora=[]
	num_pessoas_total = 0
	for obj in numero_pessoas:
		datahora = Datahora.objects.filter(id = obj.datahora_id)
		horario = str(datahora[0].dia)+"/"+str(datahora[0].mes)+","+ str(datahora[0].hora)+":"+str(datahora[0].minutos)
		lista_datahora.append([horario, obj.num_de_pessoas])
		num_pessoas_total+=obj.num_de_pessoas
	media_pessoas = num_pessoas_total/len(numero_pessoas)
	media_lotacao = media_pessoas/0.8
	numero_fila = 0
	local_fila = Local.objects.filter(tipo = "fila")
	tempo = 0
	lista_pessoas_ids = []
	lista_pessoas_ids_rest = []
	for local in local_fila:
		local_xmax = local.x + local.width
		local_ymax = local.y + local.height
		posicoes_no_local = Posicao.objects.filter(x__gte = local.x , x__lte = local_xmax, y__gte = local.y, y__lte = local_ymax, atual = 1)
		numero_fila +=len(posicoes_no_local)
	for local in local_fila:
		local_xmax = local.x + local.width
		local_ymax = local.y + local.height
		posicoes_no_local_total = Posicao.objects.filter(x__gte = local.x , x__lte = local_xmax, y__gte = local.y, y__lte = local_ymax, atual = 0)
		for posicao_total in posicoes_no_local_total:
			tempo += (posicao_total.instante_final - posicao_total.instante_inicial)
			lista_pessoas_ids.append(posicao_total.pessoa_id)
	total_pessoas_fila = len(set(lista_pessoas_ids))
	tempo_medio = int((tempo/total_pessoas_fila)/100)
	#ultimo = len(numero_pessoas)
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