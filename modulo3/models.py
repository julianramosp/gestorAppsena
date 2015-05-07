#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import smart_unicode
#Tablas modulo 3


#Tabla Listado Maquina
class Maquina(models.Model):
    NombreRecurso = models.CharField(max_length=100, default = '')
    Descripcion = models.TextField(null = True)
    Imagen = models.ImageField(upload_to='static/files',null=True,blank=True)#error al consultar pilas al momento de la consulta
    Precio = models.DecimalField(max_digits=20,decimal_places=2)
    def __unicode__(self):
        return smart_unicode(self.NombreRecurso)

class Tipo_De_Dia(models.Model):
    TIPO_DIA =(
    ('Jornada Convencional','Jornada Convencional'),
    ('Jornada Sabados','Jornada Sabados'),
    ('Jornada Especial Lunes','Jornada Especial Lunes'),
    ('Jornada Especial Martes','Jornada Especial Martes'),
    ('Jornada Especial Miercoles','Jornada Especial Miercoles'),
    ('Jornada Especial Jueves','Jornada Especial Jueves'),
    ('Jornada Especial Viernes','Jornada Especial Viernes'),
    ('Jornada Especial Sabado','Jornada Especial Sabado'),
    ('Jornada Especial Domingo','Jornada Especial Domingo'),
    )
    Jornada = models.CharField(max_length =50, choices=TIPO_DIA,null=True,blank=True)
    def __unicode__(self):
        return smart_unicode(self.Jornada)

class Franja_Jornada(models.Model):
    FRANJA_TIEMPO =(
    ('Primera Parte Manana','Primera Parte Manana'),
    ('Segunda Parte Manana','Segunda Parte Manana'),
    ('Descanso-Almuerzo','Descanso-Almuerzo'),
    ('Primera Parte Tarde','Primera Parte Tarde'),
    ('Segunda Parte Tarde','Segunda Parte Tarde'),
    ('Primera Parte Noche','Primera Parte Noche'),
    ('Segunda Parte Noche','Segunda Parte Noche'),
    )
    Franja_De_Tiempo = models.CharField(max_length=100, choices = FRANJA_TIEMPO, default='0')
    Descanso = models.BooleanField(default = False)
    def __unicode__ (self):
       return smart_unicode(self.Franja_De_Tiempo)
	   

class Dia_Laboral(models.Model):
    Tipo_De_Dia = models.ForeignKey(Tipo_De_Dia, null=True, blank=True)
    Total = models.IntegerField(max_length=5, default=0,null=True, blank=True)
    def __unicode__(self):
        return smart_unicode(self.Tipo_De_Dia)

class Jornada_Laboral(models.Model):
    Tipo_De_Dia = models.ForeignKey(Dia_Laboral,null=True, blank=True)
    Franja_De_Tiempo= models.ForeignKey(Franja_Jornada,null=True, blank=True)
    Tiempo_Inicio = models.TimeField(auto_now= 0, auto_now_add= 0, default=0)
    Tiempo_Fin = models.TimeField(auto_now= 0, auto_now_add= 0, default=0)
    SubTotal = models.IntegerField(max_length=5, default=0 )#Tiempo_Inicio-Tiempo_Final
    def __unicode__(self):
        return smart_unicode(self.Tipo_De_Dia)




class Suplemento_Fisico(models.Model):
    FISICO = (
    (0,0),
    (3,3),
    (5,5),
    (7,7),
    )
    S_Fisico = models.DecimalField(max_digits=20,decimal_places=6, null= True, blank= True)
    Descripcion = models.CharField(max_length =50, null = True)
    def __unicode__(self):
       return smart_unicode(self.S_Fisico)

class Suplemento_Mental(models.Model):
    S_Mental = models.DecimalField(max_digits=20,decimal_places=4)
    Descripcion = models.CharField(max_length =50, null = True)
    def __unicode__(self):
        return smart_unicode(self.S_Mental)

class Suplemento_Monotonia(models.Model):
    MONOTONIA = (
    (0,0),   
    (3,3),
    (5,5),
    (7,7),
    )
    S_Monotonia = models.DecimalField(max_digits=20,decimal_places=8)
    Descripcion = models.CharField(max_length =50, null = True)
    def __unicode__(self):
        return smart_unicode(self.S_Monotonia)

class Suplemento_Ambiental(models.Model):
    AMBIENTAL = (
    (0,0),   
    (3,3),
    (5,5),
    (7,7),
    )
    S_Ambiental = models.DecimalField(max_digits=20,decimal_places=4)
    Descripcion = models.CharField(max_length =50, null = True)
    def __unicode__(self):
        return smart_unicode(self.S_Ambiental)

class Suplemento_Genero(models.Model):
    GENERO= (
    (0,0),   
    (3,3),
    (5,5),
    (7,7),
    )
    S_Genero = models.DecimalField(max_digits=20,decimal_places=4)
    Descripcion = models.CharField(max_length =50, null = True)
    def __unicode__(self):
        return smart_unicode(self.S_Genero)

class Calificacion_Habilidad(models.Model):
    Habilidad= (
    (0,0),   
    (-1,-1),
    (-2,-2),
    (-3,-3),
    (-4,-4),

    )
    C_Habilidad = models.DecimalField(max_digits=20,decimal_places=4)
    Descripcion = models.CharField(max_length =50, null = True)
    def __unicode__(self):
       return smart_unicode(self.C_Habilidad)

class Calificacion_Consistencia(models.Model):
    CONSISTENCIA= (
    (4,4),   
    (3,3),
    (2,2),
    (1,1),
    (0,0),   
    (-1,-1),
    (-2,-2),
    (-3,-3),
    (-4,-4),
    )
    C_Consistencia = models.DecimalField(max_digits=20,decimal_places=4)
    Descripcion = models.CharField(max_length =50, null = True)
    def __unicode__(self):
        return smart_unicode(self.C_Consistencia)



class Calificacion_Esfuerzo(models.Model):
    ESFUERZO= (
    (4,4),   
    (3,3),
    (2,2),
    (1,1),
    (0,0),   
    (-1,-1),
    (-2,-2),
    (-3,-3),
    (-4,-4),

    )
    C_Esfuerzo = models.DecimalField(max_digits=20,decimal_places=4)
    Descripcion = models.CharField(max_length =50, null = True)
    def __unicode__(self):
        return smart_unicode(self.C_Esfuerzo)




class Generalidad_Tiempos(models.Model):
    Actividad = models.CharField(max_length= 50, null=True, blank = True)
    Tiempo_Promedio = models.TimeField(auto_now= 0, auto_now_add= 0, null= True, blank = True)
    Numero_Repeticiones = models.IntegerField(max_length= 2, default=0, null= True, blank = True)#cantidad de veces que se repite un proceso
    Tiempo_Estandard =  models.TimeField(auto_now= 0, auto_now_add= 0, null= True, blank = True)
    S_Fisico = models.ForeignKey(Suplemento_Fisico, null= True, blank = True)
    S_Mental = models.ForeignKey(Suplemento_Mental, null= True, blank = True)
    Sup_Monotonia = models.DecimalField(max_digits=20,decimal_places=4, blank = True, null = True)
    S_Ambiental = models.ForeignKey(Suplemento_Ambiental, null= True, blank = True)
    Suplemento_Genero = models.ForeignKey(Suplemento_Genero, null= True, blank = True)
    Calificacion_Habilidad = models.ForeignKey(Calificacion_Habilidad, null= True, blank = True)
    Calificacion_Consistencia = models.ForeignKey(Calificacion_Consistencia, null= True, blank = True)
    Calificacion_Esfuerzo = models.ForeignKey(Calificacion_Esfuerzo, null= True, blank = True)
    def  __unicode__ (self):
        return smart_unicode(self.Actividad)

class Tiempos_Por_Actividad(models.Model):
    Actividad = models.ForeignKey(Generalidad_Tiempos)
    Muestras_Tiempo= models.TimeField(auto_now=False, auto_now_add=False, null= True, blank=True) 
    def __unicode__(self):
        return smart_unicode(self.Actividad)


class Producto_Referencia (models.Model):#producto sobre el cual se realiza la medida de tiempo
    Nombre_Producto = models.CharField(max_length= 100,null=True, blank=True)
    Tipo_De_Dia= models.ForeignKey(Dia_Laboral,null=True, blank=True)
    Total_jornada = models.IntegerField(max_length=5, default=0,null=True, blank=True)
    Lote_A_Fabricar = models.CharField(max_length= 100 ,null=True, blank=True)
    Eficiencia = models.IntegerField(max_length= 3,null=True, blank=True, default = 0)#preguntar de donde se calcula este valor
    Tiempo_Total_lote = models.CharField(max_length =50,  null= True, blank=True) 
    Total_Recurso_humano = models.DecimalField(max_digits=20,decimal_places=2, default= 0, blank = True)
    Total_Recurso_por_actividad= models.DecimalField(max_digits=20,decimal_places=4, default= 0, blank = True)
    Suma_Tiempo_Estandard = models.CharField(max_length= 100 ,null=True, blank=True)
    def __unicode__(self):
        return smart_unicode(self.Nombre_Producto) 

class Ruta_Operacional ( models.Model):
    Nombre_producto=models.ForeignKey(Producto_Referencia,null=True, blank=True)
    Actividad = models.ForeignKey(Generalidad_Tiempos,null=True, blank=True)
    Maquina = models.ForeignKey(Maquina,null=True, blank=True)
    Precio = models.DecimalField(max_digits=20,decimal_places=4,blank= True, default=0 ,null=True)
    Tiempo_Estandard =  models.TimeField(auto_now= 0, auto_now_add= 0, null= True, blank = True)
    Tiempo_Lote=models.DecimalField(max_digits=20,decimal_places=2,blank= True, default=0 ,null=True)
    Recurso_humano = models.DecimalField(max_digits=20,decimal_places=2,blank= True, default=0)
    def __unicode__(self):
        return smart_unicode(self.id)
		

