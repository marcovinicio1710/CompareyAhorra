from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from reviews.sitemaps import Productos_Superr
from django.contrib.staticfiles.storage import staticfiles_storage

from django.views.generic.base import RedirectView

sitemaps={'productos': Productos_Superr,}

urlpatterns = [
    
    path('cr/', views.index, name='home-page'),
    path('', views.index_redirect, name='home-page-main'),
    path('cr/search_products/', views.search, name='search-product'),
    path('cr/buscar-producto/', views.search_prod, name='search-producto/'),
    path('cr/buscar-producto/<str:searched><str:categoria><str:price_kg><str:price_lt><str:price_unid><str:page>', views.search_prod, name='search-producto/'),
    path('cr/search_products_unity/', views.search_unity, name='search-unity'),
    path('cr/search_products_weight/', views.search_weight, name='search-weight'),
    path('cr/search_products_volume/', views.search_volume, name='search-volume'),
    path('cr/sign-up/', views.sign_up_page, name='sign-up'),
    path('cr/log-out/', views.log_out, name='log-out'),
    path('cr/login/', views.log_in, name='login'),
    path('cr/cart/', views.cart, name='cart'),
    path('cr/aviso-de-privacidad/', views.aviso_privacidad, name='aviso-de-privacidad'),
    path('cr/terminos-condiciones/', views.terminosYcondiciones, name='terminos-condiciones'),
    path('cr/preguntas-frequentes/', views.preguntasfrequentes, name='preguntas-frequentes'),
    path('cr/canasta-basica/', views.canastabasica, name='canasta-basica'),
    path('cr/recuperar-password/', views.recovery_password, name='recuperar-password'),
    path('cr/nuestros-servicios/', views.publicidad_interna, name='nuestros-servicios'),
    
    path('productos/<int:id>', views.post_producto, name='post'),
    path('cr/sobre-nos/', views.sobrenos, name='sobre-nos'),
    path('ads.txt', views.hooligan, name='hooligan'),
    path("sitemap.xml",views.site_map,name='site-map'),
    path("test-hooligan/",views.test_ads,name='test-hooligan'),
    #path("ads.txt",RedirectView.as_view(url=staticfiles_storage("ads.txt"))),
 
   
]

if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

