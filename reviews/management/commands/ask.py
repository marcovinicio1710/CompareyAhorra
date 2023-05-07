import pandas as pd

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from reviews.models import Productos_Super
from datetime import datetime
import os
from pathlib import Path
from django.contrib.auth.models import User

now = datetime.now()
now=str(now)
lista_now=now.split()
noww=lista_now[0]
print(now)

print('1 para ver cuanto producto tienes hoy')
print('2 para saber cuanto usuaruis estan creados')
a=input('selecciona una opcion')

if a=='1':
    
    lista=Productos_Super.objects.filter(fecha=noww)
    print('aqui esta los product del dia')
    print(len(lista))
elif a=='2':
    lista=User.objects.all()
    print('los usuarios creados son:')
    print(len(lista))
else:
    print('lo siento no se selecciono correcto')