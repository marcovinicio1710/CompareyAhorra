from django.db import models
from django.contrib import auth
from django.urls import reverse

# Create your models here.

class Productos_Super(models.Model):
    super = models.CharField(max_length=50, help_text="The name of the Supermarket.")
    categoria = models.CharField(max_length=50, help_text="The name of the Category.")
    producto = models.CharField(max_length=300 , help_text="The name of the Product.")
    precio = models.FloatField(help_text="The price of product")
    picture = models.URLField(max_length=300 , help_text="Picture of the product.")
    peso_kg = models.FloatField(help_text="peso kg")
    precio_kg = models.FloatField( help_text="peso kg")
    peso_lt = models.FloatField( help_text="peso lt")
    precio_lt = models.FloatField( help_text="peso lt")
    peso_unidad = models.FloatField( help_text="unidad")
    precio_unidad = models.FloatField( help_text="precio unidad")
    fecha = models.DateField( help_text="fecha ingreso", default="2023-03-17")

    def __str__(self):
        return (self.super+' '+self.producto)
    
    def get_absolute_url(self):
        return(reverse('post', args=[str(self.id)]))

class Carrito_compra(models.Model):
    #A published book.
    email = models.EmailField(help_text="The User's email address.")
    
    publisher = models.ForeignKey(Productos_Super,
                                  on_delete=models.CASCADE)
    

    def __str__(self):
        return (self.email + self.publisher)

class Publisher(models.Model):
    #A company that publishes books."""

    name = models.CharField(max_length=50, help_text="The name of the Publisher.")
    website = models.URLField(help_text="The Publisher's website.")
    email = models.EmailField(help_text="The Publisher's email address.")
    def __str__(self):
        return self.name+self.website

class Book(models.Model):
    #A published book.
    title = models.CharField(max_length=70,
                             help_text="The title of the book.")
    publication_date = models.DateField(
        verbose_name="Date the book was published.")
    isbn = models.CharField(max_length=20,
                            verbose_name="ISBN number of the book.")
    publisher = models.ForeignKey(Publisher,
                                  on_delete=models.CASCADE)
    contributors = models.ManyToManyField('Contributor',
                                          through="BookContributor")

    def __str__(self):
        return self.title



class Contributor(models.Model):
    #A contributor to a Book, e.g. author, editor, co-author.
    first_names = models.CharField(max_length=50,
                                   help_text="The contributor's first name or names.")
    last_names = models.CharField(max_length=50,
                                  help_text="The contributor's last name or names.")
    email = models.EmailField(help_text="The contact email for the contributor.")

    def __str__(self):
        return self.first_names


class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        AUTHOR = "AUTHOR", "Author"
        CO_AUTHOR = "CO_AUTHOR", "Co-Author"
        EDITOR = "EDITOR", "Editor"

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    role = models.CharField(verbose_name="The role this contributor had in the book.",
                            choices=ContributionRole.choices, max_length=20)


class Review(models.Model):
    content = models.TextField(help_text="The Review text.")
    rating = models.IntegerField(help_text="The rating the reviewer has given.")
    date_created = models.DateTimeField(auto_now_add=True,
                                        help_text="The date and time the review was created.")
    date_edited = models.DateTimeField(null=True,
                                       help_text="The date and time the review was last edited.")
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             help_text="The Book that this review is for.") 
    
class Publicidad_interesados(models.Model):
    #A company that publishes books."""

    name = models.CharField(max_length=50, help_text="The name of the Publisher.")
    phone=models.IntegerField(help_text="The rating the reviewer has given.")
    empresa = models.CharField(max_length=50, help_text="The name of the Publisher.")
    email = models.EmailField(help_text="The Publisher's email address.")
    def __str__(self):
        return self.name+self.phone+self.email
