import pandas as pd

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from reviews.models import Productos_Super
from datetime import datetime
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

pathh=os.getcwd()
print(pathh)
print('this is path')
now = datetime.now()
now=str(now)
lista_now=now.split()
now=lista_now[0]
print(datetime.now(), 'esta la hora de aqui')

def leer_master_12_atributtes(file,atributtes):
    list_atrr=atributtes.split(',')
    num1=list_atrr[0]
    num2=list_atrr[1]
    num3=list_atrr[2]
    num4=list_atrr[3]
    num5=list_atrr[4]
    num6=list_atrr[5]
    num7=list_atrr[6]
    num8=list_atrr[7]
    num9=list_atrr[8]
    num10=list_atrr[9]
    num11=list_atrr[10]
    num12=list_atrr[11]
    df= pd.read_excel(file)
    ip=df[[num1,num2,num3,num4,num5,num6,num7,num8,num9,num10,num11,num12]]
    vals=ip.values
    lista=vals.tolist()
    
    return(lista)

file=pathh+'/reviews/management/commands/tabla_precio_super_2023.xlsx'
num=0
total=0
lista_prod=leer_master_12_atributtes(file,'Super,Categ,Producto,Precio,Espacio_5,Espacio_6,Precios_kg,Peso_kg,Precios_lt,Peso_lt,Precios_unid,Unid')


for i in lista_prod:
    #print(len(Productos_Super.objects.all()), 'total ya guardados en database1')
    
    Super=i[0]
    Categ=i[1]
    Producto=i[2]
    Precio=float(i[3])
    Espacio_5=str(i[4])
    Espacio_6=str(i[5])
    Precios_kg=str(i[6])
    Peso_kg=str(i[7])
    Precios_lt=str(i[8])
    Peso_lt=str(i[9])
    Precios_unid=str(i[10])
    Unid=str(i[11])

    if Precios_kg=='none' or Precios_kg==0 or Peso_kg=='none' or Peso_kg==0:
        Peso_kg=0
        Precios_kg=0
    if Precios_lt=='none' or Precios_lt==0 or Peso_lt=='none' or Peso_lt==0:
        Precios_lt=0
        Peso_lt=0
    if Precios_unid=='none' or Precios_unid==0 or Unid=='none' or Unid==0:
        Precios_unid=0
        Unid=0

    b, created = Productos_Super.objects.get_or_create(super=Super,
                    categoria=Categ,
                    producto=Producto,
                    precio = Precio,
                    picture = Espacio_5,
                    peso_kg = Peso_kg,
                    precio_kg = Precios_kg,
                    peso_lt = Peso_lt,
                    precio_lt = Precios_lt,
                    peso_unidad = Unid,
                    precio_unidad = Precios_unid,
                    fecha=now)
    if created:
        num+=1
        
    total+=1
    if total%1000==0:
        print (total,'leidos', num, 'creados', len(lista_prod))
    elif total==1:
         print (total,'leidos', num, 'creados', len(lista_prod))
print( 'se cargaron ',num,'en database')