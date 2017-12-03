from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Datahora(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    dia = models.IntegerField(db_column='Dia', blank=True, null=True)  # Field name made lowercase.
    mes = models.IntegerField(db_column='Mes', blank=True, null=True)  # Field name made lowercase.
    ano = models.IntegerField(db_column='Ano', blank=True, null=True)  # Field name made lowercase.
    hora = models.IntegerField(db_column='Hora', blank=True, null=True)  # Field name made lowercase.
    minutos = models.IntegerField(db_column='Minutos', blank=True, null=True)  # Field name made lowercase.
    segundos = models.IntegerField(db_column='Segundos', blank=True, null=True)  # Field name made lowercase.
    milissegundos = models.IntegerField(db_column='Milissegundos', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DataHora'


class Local(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    nome = models.IntegerField(db_column='Nome', blank=True, null=True)  # Field name made lowercase.
    tipo = models.TextField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.
    x = models.IntegerField(db_column='X', blank=True, null=True)  # Field name made lowercase.
    y = models.IntegerField(db_column='Y', blank=True, null=True)  # Field name made lowercase.
    width = models.IntegerField(db_column='Width', blank=True, null=True)  # Field name made lowercase.
    height = models.IntegerField(db_column='Height', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Local'


class Medidafinal(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    width = models.IntegerField(db_column='Width', blank=True, null=True)  # Field name made lowercase.
    height = models.IntegerField(db_column='Height', blank=True, null=True)  # Field name made lowercase.
    #quadranteid = models.ForeignKey(Quadrantes)

    class Meta:
        managed = False
        db_table = 'MedidaFinal'


class Numeropessoasquadrante(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    num_de_pessoas = models.IntegerField(db_column='Num_de_Pessoas', blank=True, null=True)  # Field name made lowercase.
    datahora_id = models.ForeignKey(Datahora)
    #quadranteid = models.ForeignKey(Quadrantes)

    class Meta:
        managed = False
        db_table = 'NumeroPessoasQuadrante'

class Numeropessoastotal(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    num_de_pessoas = models.IntegerField(db_column='Num_de_Pessoas', blank=True, null=True)  # Field name made lowercase.
    datahora_id = models.IntegerField(db_column='Datahora_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NumeroPessoasTotal'

