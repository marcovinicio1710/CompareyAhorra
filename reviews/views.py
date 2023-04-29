from django.shortcuts import render , redirect
from reviews.models import Productos_Super , Carrito_compra, Publicidad_interesados
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from operator import itemgetter
from django.conf import settings
import os
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from math import ceil
import locale
from datetime import datetime, timedelta
# Create your views here.
def index(request):

    if request.method=='GET':
        noww=datetime.now()
        now=str(noww)
        lista_now=now.split()
        hora=lista_now[1]
        lista_hora=hora.split(':')
        horaa=int(lista_hora[0])
        '''if horaa<14:
            d = str(noww - timedelta(days=1))
            lista_d=d.split()
            hoy=lista_d[0]
        else:
            hoy=lista_now[0]'''
        if horaa<14:
            d = str(noww - timedelta(days=4))
            lista_d=d.split()
            hoy=lista_d[0]
        else:
            ##hoy=lista_now[0]  original
            d = str(noww - timedelta(days=4))
            lista_d=d.split()
            hoy=lista_d[0]

        name = " "
        lista_prod=[]
        lista_producto=[]
        lista_categoria=[]
        lista_categoria_2=[]
        lista_final_categoria=[]
        lista_final_productos=[]
        lista_categoria_1=['ABARROTES','ALIMENTOS CONGELADOS','ALIMENTOS PREPARADOS ',
                    'ARTICULOS PARA EL HOGAR','BEBES Y NINOS ','CARNES FRIAS',
                    'CARNES Y PESCADOS','ELECTRONICA','FARMACIA','FRUTAS Y VERDURAS',
                    'HIGIENE Y BELLEZA ','JUGOS Y BEBIDAS','LACTEOS','LICORES',
                    'LIMPIEZA Y MASCOTA','LISTO PARA LLEVAR','OFICINA','OPTICA',
                    'PANADERIA Y TORTILLERIA'
                    ]
        new_lista=[]
        lista_final_productos_commas=[]
        for i in lista_categoria_1:
            new_lista.append(i.capitalize)
    
        lista_producto=Productos_Super.objects.all()
        lista_producto=lista_producto.filter(fecha__icontains=hoy)
        #lista_producto = get_list_or_404(Productos_Super, fecha=hoy)
        for i in range(len(lista_producto)):
            cat=str(lista_producto[i].categoria)
            cat=cat.capitalize()
            lista_prod.append([lista_producto[i].super,cat,lista_producto[i].producto,lista_producto[i].precio,lista_producto[i].picture,lista_producto[i].peso_kg,round(float(lista_producto[i].precio_kg),2),lista_producto[i].peso_lt,round(float(lista_producto[i].precio_lt),2),lista_producto[i].peso_unidad, round(float(lista_producto[i].precio_unidad),2),lista_producto[i].pk])

        for lista_de_prod in lista_prod:
            lista_categoria.append(lista_de_prod[1])
            if lista_de_prod[1] not in lista_categoria_2:
                lista_categoria_2.append(lista_de_prod[1])
        lista_categoria_2=sorted(lista_categoria_2)
        for cat in lista_categoria_2:
            num=lista_categoria.count(cat)
            lista_final_categoria.append([cat,num])
        num_prod=len(lista_prod)
        lista_precio=sorted(lista_prod, key=itemgetter(3))
        for i in range(len(lista_precio)):
            if i>29:
                break
            else:
                lista_final_productos.append(lista_precio[i])
    
        try:
            nombre_pila=request.user.first_name
        except:
            nombre_pila='AnonymousUser'

    
        for i in lista_final_productos:
            superr=i[0]
            categoriaa=i[1]
            productoo=i[2]
            precioo=ceil(i[3])
            pic=i[4]
            pesokg=round(float(i[5]),3)
            preciokg=round(float(i[6]),2)
            pesolt=round(float(i[7]),2)
            preciolt=round(float(i[8]),2)
            pesoU=round(float(i[9]),2)
            precioU=round(float(i[10]),2)
            PK=i[11]
            preciooo="{:,}".format(precioo)        
            pesokg="{:,}".format(pesokg)
            preciokg="{:,}".format(preciokg)
            pesolt="{:,}".format(pesolt)
            preciolt="{:,}".format(preciolt)
            pesoU="{:,}".format(pesoU)
            precioU="{:,}".format(precioU)
            lista_final_productos_commas.append([superr,categoriaa,productoo,str(preciooo),pic,pesokg,preciokg,pesolt,preciolt,pesoU,precioU,PK])
          


        return render(request, "index_page.html", {"categoria":"all","name": name, "lista_categoria":lista_final_categoria , 'num_prod':num_prod,'lista_productos':lista_final_productos_commas,'super':'all', "nombre_pila":nombre_pila})

    elif request.method=='POST':
        if request.user.is_authenticated:
            print('*/**/*/*/*//*/*/*/')
            print(request.POST)
            urll=(request.build_absolute_uri )
            urll=str(urll)
            lista_url=urll.split()
            urll=lista_url[-1]
            urll=urll.replace(">","")
            urll=urll.replace("'","")
            
            id_producto=request.POST['carrito']
            producto=Productos_Super.objects.get(pk=id_producto)
            userr=request.user
            correo_e=userr.email
            created = Carrito_compra.objects.get_or_create(email=correo_e, publisher=producto)

            return redirect(urll) 
            # Do something for authenticated users.
        else:
            return redirect('login')
            # Do something for anonymous users.
def file_upload(request):
    name = "WORLD"
    if request.method=='POST':
        save_path = os.path.join(settings.MEDIA_ROOT, request.FILES["file-upload-name"].name)
        name_1=request.FILES["file-upload-name"].name
        print(save_path)
        with open(save_path, "wb") as output_file:

            for chunk in request.FILES["file-upload-name"].chunks():

                output_file.write(chunk)

        return render(request, "ACL_upload.html", {"name": request.method, 'MEDIA_URL':settings.MEDIA_URL, 'name_1':name_1  })

    return render(request, "ACL_upload.html", {"name": request.method, 'MEDIA_URL':settings.MEDIA_URL })

def search(request):
    lista_categoria=['ABARROTES','ALIMENTOS CONGELADOS','ALIMENTOS PREPARADOS ',
                    'ARTICULOS PARA EL HOGAR','BEBES Y NINOS ','CARNES FRIAS',
                    'CARNES Y PESCADOS','ELECTRONICA','FARMACIA','FRUTAS Y VERDURAS',
                    'HIGIENE Y BELLEZA ','JUGOS Y BEBIDAS','LACTEOS','LICORES',
                    'LIMPIEZA Y MASCOTA','LISTO PARA LLEVAR','OFICINA','OPTICA',
                    'PANADERIA Y TORTILLERIA'
                    ]
    lista_cat=[]
    lista_producto=[]
    lista_prod_fin=[]
    lista_prod_prec=[]
    name = "Escribe un producto:"
    
    if request.method == 'POST':
        print(request.POST)
        try:
            todo=request.POST['todos']
        except MultiValueDictKeyError:
            todo='no'
        if todo =='no':
            for list in lista_categoria:
                try:
                    lista_cat.append(request.POST[list])
                except MultiValueDictKeyError:
                    a='a'
            if len(lista_cat)==0:
                todo='Todos'

        searched= request.POST['searched']
        lista_search=searched.split()
        if todo=='Todos':
            lista_producto=Productos_Super.objects.all()
            for word in lista_search:
                lista_producto=lista_producto.filter(producto__icontains=word)
        else:
            lista_producto=Productos_Super.objects.filter(categoria__in=lista_cat)
            for word in lista_search:
                lista_producto=lista_producto.filter(producto__icontains=word)
                
        if len(lista_producto)>0:
            for i in range(len(lista_producto)):

                lista_prod_fin.append([lista_producto[i].super,lista_producto[i].categoria,lista_producto[i].producto,lista_producto[i].precio,lista_producto[i].picture])
            qty_prod=True
        else:
            qty_prod= False 

        lista_precio=sorted(lista_prod_fin, key=itemgetter(3))
        print('estas en search')
        return render(request, "search_bar.html", {"name": searched,'qty_prod':qty_prod , 'lista_prod_prec':lista_precio})
    else:
        return render(request, "select_bar1.html", {"name": name})

def search_prod(request, searched='',categoria='all',price_kg='no',price_lt='no', price_uni='no',page="0"):
    noww=datetime.now()
    now=str(noww)
    lista_now=now.split()
    hora=lista_now[1]
    lista_hora=hora.split(':')
    horaa=int(lista_hora[0])
    if horaa<14:
        d = str(noww - timedelta(days=4))
        lista_d=d.split()
        hoy=lista_d[0]
    else:
        ##hoy=lista_now[0]  original
        d = str(noww - timedelta(days=4))
        lista_d=d.split()
        hoy=lista_d[0]

    lista_prod=[]
    lista_categoria=[]
    lista_categoria_2=[]
    lista_final_categoria=[]
    lista_final_productos=[]
    lista_final_productos_commas=[]
    lista_pagina=[]
    lista_param_page=["disabled",1,2]
    if request.method=='GET':

        """print('*/**/*/*/*//*/*/*/')
        print(request.GET)
        urll=(request.build_absolute_uri )
        urll=str(urll)
        lista_url=urll.split()
        urll=lista_url[-1]
        urll=urll.replace(">","")
        urll=urll.replace("'","")
        print(urll)
        print(type(urll))"""
        values= list(request.GET.keys())
        if 'searched' in values:
            searched=request.GET['searched']
            
            list_charc=[['Á','A'],['á','a'],['É','E'],['é','e'],['Í','I'],['í','i'],['Ó','O']
                        ,['ó','O'],['Ñ','N'],['ñ','n'],['Ü','U'],['ü','u'],['Ú','U'],['ú','u']]

            for char in list_charc:
                searched=searched.replace(char[0],char[1])
        
        if 'categoria' in values:
            categoria=request.GET['categoria'].upper()
        if 'page' in values:
            page=request.GET['page']
        

        lista_search=searched.split()
        if categoria=='all' or categoria=='ALL':
            
            lista_producto=Productos_Super.objects.filter(fecha__icontains=hoy)
            
            for word in lista_search:
                lista_producto=lista_producto.filter(producto__icontains=word)
        else:
            lista_producto=Productos_Super.objects.filter(fecha__icontains=hoy)
            
            lista_producto=lista_producto.filter(categoria__icontains=categoria)
            for word in lista_search:
                lista_producto=lista_producto.filter(producto__icontains=word)

        for i in range(len(lista_producto)):
            prices=round(float(lista_producto[i].precio),3)
            if prices<9999999:
                cat=str(lista_producto[i].categoria)
                cat=cat.capitalize()
                lista_prod.append([lista_producto[i].super,cat,lista_producto[i].producto,prices,lista_producto[i].picture,lista_producto[i].peso_kg,round(float(lista_producto[i].precio_kg),2),lista_producto[i].peso_lt,round(float(lista_producto[i].precio_lt),2),lista_producto[i].peso_unidad, round(float(lista_producto[i].precio_unidad),2),lista_producto[i].pk])

        for lista_de_prod in lista_prod:
            lista_categoria.append(lista_de_prod[1])
            if lista_de_prod[1] not in lista_categoria_2:
                lista_categoria_2.append(lista_de_prod[1])

        lista_categoria_2=sorted(lista_categoria_2)
        for cat in lista_categoria_2:
            num=lista_categoria.count(cat)
            lista_final_categoria.append([cat,num])

        num_prod=len(lista_prod)
        
        if page=="0":
            
            if len(lista_prod)<31:
                page="1"
            else:
                paginas=len(lista_prod)/30
                paginas=ceil(paginas)
                if paginas>7:
                    for i in range(7):
                        lista_pagina.append(str(i+1))
                    lista_pagina.append("...")
                    lista_pagina.append(str(paginas))   
                    prev_page="disabled"
                    next="2"
                    page="1"
                    lista_param_page=[prev_page,page,next]
                else:
                    for i in range(paginas):
                        lista_pagina.append(str(i+1))
                      
                    prev_page="disabled"
                    next="2"
                    page="1"
                    lista_param_page=[prev_page,page,next]

        else:
                paginas=len(lista_prod)/30
                paginas=ceil(paginas)

                if int(page)>8 and (paginas-int(page))>=4:
                    for i in range(int(page)-4, int(page)+4) :
                        lista_pagina.append(str(i+1))
                elif int(page)>8 and (paginas-int(page))<4:
                    for i in range(int(page)-7, paginas) :
                        lista_pagina.append(str(i+1))
                elif int(page)<8 and paginas>7:
                    for i in range(7):
                        lista_pagina.append(str(i+1))
                    lista_pagina.append("...")
                    lista_pagina.append(str(paginas))  
                else:
                    for i in range(paginas):
                        lista_pagina.append(str(i+1))

                if page=="1":
                    prev_page="disabled"
                else:
                    prev_page=(int(page)-1)
                if str(paginas)==page:
                    next="disabled"
                else:
                    next=int(page)+1
                
                lista_param_page=[prev_page,page,next]



        if 'price_kg' in values:
            price_kg="yes"
            lista_precio=sorted(lista_prod, key=itemgetter(6))
            for i in range(len(lista_precio)):
                if float(lista_precio[i][6])>1:
                    lista_final_productos.append(lista_precio[i])
            if len(lista_final_productos)>30:
                if str(page)==str(next):

                    lista_final_productos=lista_final_productos[(int(page)*30)-30:]
                else:

                    lista_final_productos=lista_final_productos[(int(page)*30)-30:(int(page)*30)]
        elif 'price_lt' in values:
            price_lt="yes"
            
            lista_precio=sorted(lista_prod, key=itemgetter(8))
            for i in range(len(lista_precio)):
                if float(lista_precio[i][8])>1:
                    lista_final_productos.append(lista_precio[i])
            if len(lista_final_productos)>30:
                if str(page)==str(next):

                    lista_final_productos=lista_final_productos[(int(page)*30)-30:]
                else:

                    lista_final_productos=lista_final_productos[(int(page)*30)-30:(int(page)*30)]
        
        elif 'price_unid' in values:
            price_unid="yes"
            
            lista_precio=sorted(lista_prod, key=itemgetter(10))
            for i in range(len(lista_precio)):
                if float(lista_precio[i][10])>1:
                    lista_final_productos.append(lista_precio[i])
            if len(lista_final_productos)>30:
                if str(page)==str(next):

                    lista_final_productos=lista_final_productos[(int(page)*30)-30:]
                else:

                    lista_final_productos=lista_final_productos[(int(page)*30)-30:(int(page)*30)]
        else:

            lista_precio=sorted(lista_prod, key=itemgetter(3))

            for i in range(len(lista_precio)):
                lista_final_productos.append(lista_precio[i])
            if len(lista_final_productos)>30:
                if str(page)==str(next):

                    lista_final_productos=lista_final_productos[(int(page)*30)-30:]
                else:

                    lista_final_productos=lista_final_productos[(int(page)*30)-30:(int(page)*30)]
        
        if len(lista_prod)<31:
            page_bool="no"
        else:
            page_bool="yes"
        try:
            nombre_pila=request.user.first_name
        except:
            nombre_pila='AnonymousUser'
        name=searched

        for i in lista_final_productos:
            superr=i[0]
            categoriaa=i[1]
            productoo=i[2]
            precioo=ceil(i[3])
            pic=i[4]
            pesokg=round(float(i[5]),3)
            preciokg=round(float(i[6]),2)
            pesolt=round(float(i[7]),2)
            preciolt=round(float(i[8]),2)
            pesoU=round(float(i[9]),2)
            precioU=round(float(i[10]),2)
            PK=i[11]
            preciooo="{:,}".format(precioo)        
            pesokg="{:,}".format(pesokg)
            preciokg="{:,}".format(preciokg)
            pesolt="{:,}".format(pesolt)
            preciolt="{:,}".format(preciolt)
            pesoU="{:,}".format(pesoU)
            precioU="{:,}".format(precioU)
            lista_final_productos_commas.append([superr,categoriaa,productoo,str(preciooo),pic,pesokg,preciokg,pesolt,preciolt,pesoU,precioU,PK])
            
        
        return render(request, "search_producto.html", {"categoria":categoria, "name": name, "lista_categoria":lista_final_categoria , 'num_prod':num_prod,'lista_productos':lista_final_productos_commas,"page":page, "page_bool":page_bool, "lista_pagina":lista_pagina , "lista_param_page":lista_param_page, "price_kg":price_kg,"price_lt":price_lt, "price_uni":price_uni, "nombre_pila":nombre_pila })
    
    elif request.method=='POST':
        if request.user.is_authenticated:
            print('*/**/*/*/*//*/*/*/')
            print(request.POST)
            urll=(request.build_absolute_uri )
            urll=str(urll)
            lista_url=urll.split()
            urll=lista_url[-1]
            urll=urll.replace(">","")
            urll=urll.replace("'","")
            
            id_producto=request.POST['carrito']
            producto=Productos_Super.objects.get(pk=id_producto)
            userr=request.user
            correo_e=userr.email
            created = Carrito_compra.objects.get_or_create(email=correo_e, publisher=producto)

            return redirect(urll) 
            # Do something for authenticated users.
        else:
            return redirect('login')
            # Do something for anonymous users.
        
def search_unity(request):
    lista_categoria=['ABARROTES','ALIMENTOS CONGELADOS','ALIMENTOS PREPARADOS ',
                    'ARTICULOS PARA EL HOGAR','BEBES Y NINOS ','CARNES FRIAS',
                    'CARNES Y PESCADOS','ELECTRONICA','FARMACIA','FRUTAS Y VERDURAS',
                    'HIGIENE Y BELLEZA ','JUGOS Y BEBIDAS','LACTEOS','LICORES',
                    'LIMPIEZA Y MASCOTA','LISTO PARA LLEVAR','OFICINA','OPTICA',
                    'PANADERIA Y TORTILLERIA'
                    ]
    lista_cat=[]
    lista_producto=[]
    lista_prod_fin=[]
    lista_prod_prec=[]
    name = "Escribe un producto:"
    especifico="Catergoria de Unidad"
    
    if request.method == 'POST':
        print(request.POST)
        try:
            todo=request.POST['todos']
        except MultiValueDictKeyError:
            todo='no'
        if todo =='no':
            for list in lista_categoria:
                try:
                    lista_cat.append(request.POST[list])
                except MultiValueDictKeyError:
                    a='a'
            if len(lista_cat)==0:
                todo='Todos'

        searched= request.POST['searched']
        lista_search=searched.split()
        if todo=='Todos':
            lista_producto=Productos_Super.objects.all()
            for word in lista_search:
                lista_producto=lista_producto.filter(producto__icontains=word)
        else:
            lista_producto=Productos_Super.objects.filter(categoria__in=lista_cat)
            for word in lista_search:
                lista_producto=lista_producto.filter(producto__icontains=word)
                
        if len(lista_producto)>0:
            for i in range(len(lista_producto)):
                if float(lista_producto[i].precio_unidad) > 1:
                    lista_prod_fin.append([lista_producto[i].super,lista_producto[i].categoria,lista_producto[i].producto,lista_producto[i].precio,lista_producto[i].picture,round(float(lista_producto[i].precio_unidad),2)])
            qty_prod=True
        else:
            qty_prod= False 

        lista_precio=sorted(lista_prod_fin, key=itemgetter(5))
        

        return render(request, "search_unidad_post.html", {"name": searched,'qty_prod':qty_prod , 'lista_prod_prec':lista_precio})
    else:
        return render(request, "search_unidad_get.html", {"name": name, "especifico": especifico})

def search_weight(request):
    lista_categoria=['ABARROTES','ALIMENTOS CONGELADOS','ALIMENTOS PREPARADOS ',
                    'ARTICULOS PARA EL HOGAR','BEBES Y NINOS ','CARNES FRIAS',
                    'CARNES Y PESCADOS','ELECTRONICA','FARMACIA','FRUTAS Y VERDURAS',
                    'HIGIENE Y BELLEZA ','JUGOS Y BEBIDAS','LACTEOS','LICORES',
                    'LIMPIEZA Y MASCOTA','LISTO PARA LLEVAR','OFICINA','OPTICA',
                    'PANADERIA Y TORTILLERIA'
                    ]
    lista_cat=[]
    lista_producto=[]
    lista_prod_fin=[]
    lista_prod_prec=[]
    name = "Escribe un producto:"
    especifico="Catergoria de Peso"
    
    if request.method == 'POST':
        
        print(request.POST)
        try:
            todo=request.POST['todos']
        except MultiValueDictKeyError:
            todo='no'
        if todo =='no':
            for list in lista_categoria:
                try:
                    lista_cat.append(request.POST[list])
                except MultiValueDictKeyError:
                    a='a'
            if len(lista_cat)==0:
                todo='Todos'

        searched= request.POST['searched']
        lista_search=searched.split()
        if todo=='Todos':
            lista_producto=Productos_Super.objects.all()
            for word in lista_search:
                lista_producto=lista_producto.filter(producto__icontains=word)
        else:
            lista_producto=Productos_Super.objects.filter(categoria__in=lista_cat)
            for word in lista_search:
                lista_producto=lista_producto.filter(producto__icontains=word)
                
        if len(lista_producto)>0:
            for i in range(len(lista_producto)):
                
                if float(lista_producto[i].precio_kg) > 1:
                    
                    lista_prod_fin.append([lista_producto[i].super,lista_producto[i].categoria,lista_producto[i].producto,lista_producto[i].precio,lista_producto[i].picture,round(float(lista_producto[i].precio_kg),2)])
            qty_prod=True
        else:
            qty_prod= False 

        lista_precio=sorted(lista_prod_fin, key=itemgetter(5))
        
        return render(request, "search_peso_post.html", {"name": searched,'qty_prod':qty_prod , 'lista_prod_prec':lista_precio})
    else:
        return render(request, "get_search_peso.html", {"name": name, "especifico": especifico})


def search_volume(request):
    
    lista_categoria=['ABARROTES','ALIMENTOS CONGELADOS','ALIMENTOS PREPARADOS ',
                    'ARTICULOS PARA EL HOGAR','BEBES Y NINOS ','CARNES FRIAS',
                    'CARNES Y PESCADOS','ELECTRONICA','FARMACIA','FRUTAS Y VERDURAS',
                    'HIGIENE Y BELLEZA ','JUGOS Y BEBIDAS','LACTEOS','LICORES',
                    'LIMPIEZA Y MASCOTA','LISTO PARA LLEVAR','OFICINA','OPTICA',
                    'PANADERIA Y TORTILLERIA'
                    ]
    lista_cat=[]
    lista_producto=[]
    lista_prod_fin=[]
    lista_prod_prec=[]
    name = "Escribe un producto:"
    especifico="Catergoria de Volumen"
    
    if request.method == 'POST':
        
        print(request.POST)
        try:
            todo=request.POST['todos']
        except MultiValueDictKeyError:
            todo='no'
        if todo =='no':
            for list in lista_categoria:
                try:
                    lista_cat.append(request.POST[list])
                except MultiValueDictKeyError:
                    a='a'
            if len(lista_cat)==0:
                todo='Todos'

        searched= request.POST['searched']
        lista_search=searched.split()
        if todo=='Todos':
            lista_producto=Productos_Super.objects.all()
            for word in lista_search:
                lista_producto=lista_producto.filter(producto__icontains=word)
        else:
            lista_producto=Productos_Super.objects.filter(categoria__in=lista_cat)
            for word in lista_search:
                lista_producto=lista_producto.filter(producto__icontains=word)
                
        if len(lista_producto)>0:
            for i in range(len(lista_producto)):
                
                if float(lista_producto[i].precio_lt) > 1:
                    
                    lista_prod_fin.append([lista_producto[i].super,lista_producto[i].categoria,lista_producto[i].producto,lista_producto[i].precio,lista_producto[i].picture,round(float(lista_producto[i].precio_lt),2)])
            qty_prod=True
        else:
            qty_prod= False 

        lista_precio=sorted(lista_prod_fin, key=itemgetter(5))
        
        return render(request, "search_bar_valor.html", {"name": searched,'qty_prod':qty_prod , 'lista_prod_prec':lista_precio})
    else:
        return render(request, "get_search_especifico.html", {"name": name, "especifico": especifico})

def sign_up_page(request):
    if request.method=='POST':
        name = "POST"
        error=''
        error_pass=''
        error_email=''
        main_error=''
        
        usuario_name=request.POST["username"]
        usuario_lastname=request.POST["Lastname"]
        usuario_email=request.POST["email_address"]
        usuario_pass1=request.POST["password_1"]
        usuario_pass2=request.POST["password_2"]
        
        s = usuario_pass1
        if (len(s) >= 8):
            
            print("Valid Password Format")
            error='Valid Password Format'
        else:
            print("Invalid Password Format")
            error='Formato invalido de contraseña'
            
        if error=='Valid Password Format':
            if usuario_pass1==usuario_pass2:
                error_pass='passwords equal'
            else:
                error_pass='passwords not equal'
        if error_pass=='passwords equal':
            print('saving user')
            saved='yes'
            try:
                user= User.objects.create(username=usuario_email, password=usuario_pass1,email=usuario_email,first_name=usuario_name, last_name=usuario_lastname)
                user.save()
                login(request, user)
                return redirect('home-page')
            except IntegrityError:
                main_error='User already created, Try login.'
                return render(request, "sign_up_page.html", {"name": name ,'error':main_error})
            except :
                main_error='Error have been raised, Try again or Login.'
                return render(request, "sign_up_page.html", {"name": name ,'error':main_error})
        else:
            print("i am will not save this crazy user")
            saved='no'
            if error=='Invalid Password Format':
                main_error+='Contraseña tiene 7 o menos caracteres, Por Favor intente de nuevo. '
            if error_pass=='passwords not equal':
                main_error+='Contraseñas no son iguales, Por Favor Intente nuevamente. '
            
        print(usuario_name,usuario_lastname)
        print(usuario_email)
        print(usuario_pass1, usuario_pass2)

        return render(request, "sign_up_page.html", {"name": name ,'error':main_error})
    elif request.method=='GET':
        name='GET'
        return render(request, "sign_up_page.html", {"name": name, 'form':UserCreationForm })
    
def log_out(request):
    logout(request)
    return redirect('home-page')

def log_in(request):
    if request.method=='POST':
        usuario_email=request.POST["email_address"]
        usuario_pass1=request.POST["password_1"]
        try:
            user = User.objects.get(email=usuario_email)
            if user.password==usuario_pass1:
                # A backend authenticated the credentials
                login(request, user)
                return redirect('home-page')
            else:
                # No backend authenticated the credentials
                error="Correo electronico o contraseña no coinciden, Por favor intente de nuevo."
                return render(request, "login_page.html", {"error": error})
        except User.DoesNotExist:
            error="Correo electronico o contraseña no coinciden, Por favor intente de nuevo."
            return render(request, "login_page.html", {"error": error})

    else:
        return render(request, "login_page.html")
def recovery_password(request):
    if request.method=='POST':
        
        usuario_name=request.POST["name"]
        usuario_lastname=request.POST["lastname"]
        usuario_email=request.POST["email_address"]
        usuario_pass1=request.POST["password_1"]
        usuario_pass2=request.POST["password_2"]
        usuario_lastname=usuario_lastname.lower()
        usuario_name=usuario_name.lower()
        
        s = usuario_pass1
        if (len(s) >= 8):
            
           
            error='Valid Password Format'
        else:
           
            error='Formato invalido de contraseña'
            return render(request, "recuperarpassword.html", {"error": error})
            
        if error=='Valid Password Format':
            if usuario_pass1==usuario_pass2:
                error_pass='passwords equal'
            else:
                error_pass='contraseña no son iguales'
                return render(request, "recuperarpassword.html", {"error": error})
        if error_pass=='passwords equal':
            #comparing user
            try:
                user = User.objects.get(email=usuario_email)
                
                
                
                if user.first_name.lower()==usuario_name and user.last_name.lower()==usuario_lastname :
                    User.objects.filter(email=usuario_email). update(password=usuario_pass1)
                    
                    error="Se cambio correctamente la contraseña. Inicia Sesion nuevamente."
                    return render(request, "recuperarpassword.html", {"error": error})

                    # A backend authenticated the credentials
                    
                    
                else:
                    # No backend authenticated the credentials
                    error="Correo electronico, usuario o contraseña no coinciden, Por favor intente de nuevo."
                    return render(request, "recuperarpassword.html", {"error": error})
            except User.DoesNotExist:
                error="Correo electronico no ha sido registrado en nuestra base dato."
                return render(request, "recuperarpassword.html", {"error": error})

    else:
        return render(request, "recuperarpassword.html")

def cart(request ):
    superr='all'
    url_wall="https://www.walmart.co.cr/"
    url_AM="https://www.automercado.cr/buscar?q="
    url_PS="https://www.pricesmart.com/site/cr/es/busqueda?_sq="
    if request.user.is_authenticated:
        if request.method=='GET':
            
            values= list(request.GET.keys())
            if 'super' in values:
                
                superr=request.GET['super']

            userr=request.user
            correo_e=userr.email
            lista_carrito=Carrito_compra.objects.filter(email__contains=correo_e)
            lista_producto=[]
            lista_final_categoria=[]
            lista_final_categoria_2=[]
            sum_preci_AM=0
            sum_prec_Wall=0
            sum_prec_Pric=0
            lista_categoria_2=[]
            lista_categoria=[]
            sum_prices=0
            for i in range(len(lista_carrito)):
                
                produc=lista_carrito[i]
                
                sum_prices+=float(produc.publisher.precio)
                lista_categoria.append(produc.publisher.super)
                if produc.publisher.super not in lista_categoria_2:
                    lista_categoria_2.append(produc.publisher.super)
                    
                if produc.publisher.super=="WALLMART":
                    
                    sum_prec_Wall+=float(produc.publisher.precio)
                    url=url_wall+produc.publisher.producto
                    lista_producto.append([produc.publisher.super,produc.publisher.categoria,produc.publisher.producto,produc.publisher.precio,produc.publisher.picture,produc.pk,url])
                elif produc.publisher.super=="AUTOMERCADO":
                   
                    sum_preci_AM+=float(produc.publisher.precio)
                    url=url_AM+produc.publisher.producto
                    lista_producto.append([produc.publisher.super,produc.publisher.categoria,produc.publisher.producto,produc.publisher.precio,produc.publisher.picture,produc.pk,url])
                elif produc.publisher.super=="PRICESMART":
                    sum_prec_Pric+=float(produc.publisher.precio)
                    url=url_PS+produc.publisher.producto
                    lista_producto.append([produc.publisher.super,produc.publisher.categoria,produc.publisher.producto,produc.publisher.precio,produc.publisher.picture,produc.pk,url])
            
                
            lista_precio_total=[sum_preci_AM,sum_prec_Pric,sum_prec_Wall]
            for cat in lista_categoria_2:
                num=lista_categoria.count(cat)
                lista_final_categoria.append([cat,num])
            
            if superr=="WALLMART":
               
                for prodd in lista_producto:
                    if prodd[0]=="WALLMART":
                        lista_final_categoria_2.append(prodd)

            elif superr=="AUTOMERCADO":
                for prodd in lista_producto:
                    if prodd[0]=="AUTOMERCADO":
                        lista_final_categoria_2.append(prodd)
            elif superr=="PRICESMART":
                for prodd in lista_producto:
                    if prodd[0]=="PRICESMART":
                        lista_final_categoria_2.append(prodd)
            else:
                lista_final_categoria_2=lista_producto
            
            try:
                nombre_pila=request.user.first_name
            except:
                nombre_pila='AnonymousUser'
            
            return render(request, "carrito.html", {'num_prod':len(lista_producto) , "precio_total": sum_prices, "lista_categoria":lista_final_categoria ,"lista_productos": lista_final_categoria_2,"lista_precio_total":lista_precio_total, 'super':superr, "nombre_pila":nombre_pila})


        # Do something for authenticated users.
        elif request.method=='POST':
            values= list(request.POST.keys())
            if 'carrito' in values:
                id_producto=request.POST['carrito']
                producto=Carrito_compra.objects.get(pk=id_producto).delete()
                return redirect("cart")
            elif 'vaciar' in values:
                id_producto=request.POST['vaciar']
                userr=request.user
                correo_e=userr.email
                lista_carrito=Carrito_compra.objects.filter(email__contains=correo_e).delete()
                return redirect("cart")

    else:
        return redirect('login')
        # Do something for anonymous users.


def aviso_privacidad(request ):
    nombre_compañia="Compare y Ahorra Costa Rica"
    return render(request, "aviso_privacidad.html", {'compañia':nombre_compañia})
def terminosYcondiciones(request ):
    nombre_compañia="Compare y Ahorra Costa Rica"
    return render(request, "terminosYcondiciones.html", {'compañia':nombre_compañia})
def preguntasfrequentes(request ):
    nombre_compañia="Compare y Ahorra Costa Rica"
    return render(request, "preguntasfrequentes.html", {'compañia':nombre_compañia})
def canastabasica(request ):
    nombre_compañia="Compare y Ahorra Costa Rica"
    return render(request, "canastabasica.html", {'compañia':nombre_compañia})
def index_redirect(request):
    return redirect("home-page")

def publicidad_interna(request):
     if request.method=='GET':
        return render(request, "publicidad_interna.html")
     else:
        usuario_name=request.POST["name"]
        usuario_empresa=request.POST["empresa"]
        usuario_email=request.POST["email_address"]
        usuario_telefono=request.POST["phone"]
        created = Publicidad_interesados.objects.get_or_create(name=usuario_name,phone=usuario_telefono,empresa=usuario_empresa,email=usuario_email)
                   
        error='Muchas Gracias por elegirnos!. Pronto nos comunicaremos contigo para brindarte más información'
        return render(request, "publicidad_interna.html" , {'error':error}) 
     


def post_producto(request,producto=id):
    item=get_object_or_404(Productos_Super, id=producto)
    prod=item.producto
    return render(request, 'post_producto.html',{'post':prod})

def sobrenos(request ):
     return render(request, "sobrenos.html")

def site_map(request)  :   
    return render(request, "sitemapp.xml")
       


