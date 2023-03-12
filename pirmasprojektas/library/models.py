from django.db import models
from django.urls import reverse
import uuid
# Create your models here.

class Genre(models.Model):
    name = models.CharField("Pavadinimas", max_length=200, help_text="Iveskite knygos zanra (pvz. detektyvas)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Zanras"
        verbose_name_plural = "Zanrai"

class Book(models.Model):
    """Modelis reprezentuoja knyga"""
    title = models.CharField("Pavadinimas", max_length = 200)
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null =True, related_name = "books")
    summary = models.TextField("Aprasymas", max_length = 1000, help_text = "trumpas knygos aprasymas")
    isbn = models.CharField("ISBN", max_length = 13, help_text = "13 simboliu ... -> isbn url")
    genre=models.ManyToManyField(Genre, help_text = "Issirinkite zanra(us) siai knygai")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Nurodo konkretaus aprasymo adresa"""
        return reverse("book-detail", args = [str(self.id)])

    def display_genre(self):
        return ", ".join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = "Zanras"


class BookInstance(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, help_text = "Unikalus ID knygos kopijai")
    book = models.ForeignKey("Book", on_delete = models.SET_NULL, null = True)
    due_back = models.DateField("Bus prieinama", null = True, blank=True)

    LOAN_STATUS = (
        ("a", "Administruojama"),
        ("p", "Paimta"),
        ("g", "Galima paimti"),
        ("r", "Rezervuota")
    )

    status = models.CharField(max_length = 1, choices = LOAN_STATUS, blank = True, default = "a", help_text ="statusas")

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        return f"{self.id}  {self.book.title}"


class Author(models.Model):
    first_name = models.CharField("Vardas", max_length=1000)
    last_name = models.CharField("Pavardė", max_length=1000)
    description = models.TextField("Aprasymas", max_length = 1000, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        return reverse("author-detail", args = [str(self.id)])

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def display_books(self):
        return ", ".join(book.title for book in self.books.all()[:3])

    display_books.short_description = "Knygos"