from django.contrib.sitemaps import Sitemap
from reviews.models import Productos_Super

class Productos_Superr(Sitemap):
    def items(self) :
        return Productos_Super.objects.all()