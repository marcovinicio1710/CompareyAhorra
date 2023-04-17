from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.index, name='home-page'),
    path('search_products/', views.search, name='search-product'),
    path('buscar-producto/', views.search_prod, name='search-producto/'),
    path('buscar-producto/<str:searched><str:categoria><str:price_kg><str:price_lt><str:price_unid><str:page>', views.search_prod, name='search-producto/'),
    path('search_products_unity/', views.search_unity, name='search-unity'),
    path('search_products_weight/', views.search_weight, name='search-weight'),
    path('search_products_volume/', views.search_volume, name='search-volume'),
    path('sign-up/', views.sign_up_page, name='sign-up'),
    path('log-out/', views.log_out, name='log-out'),
    path('login/', views.log_in, name='login'),
    path('cart/', views.cart, name='cart'),
    path('aviso-de-privacidad/', views.aviso_privacidad, name='aviso-de-privacidad'),
    path('terminos-condiciones/', views.terminosYcondiciones, name='terminos-condiciones'),
    path('preguntas-frequentes/', views.preguntasfrequentes, name='preguntas-frequentes'),
     path('canasta-basica/', views.canastabasica, name='canasta-basica'),

]

if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

