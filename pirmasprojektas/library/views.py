from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Book, Author, BookInstance, Genre

# Create your views here.

def index(request):
    # Suskaičiuokime keletą pagrindinių objektų
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Laisvos knygos (tos, kurios turi statusą 'g')
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()

    # Kiek yra autorių
    num_authors = Author.objects.count()

    # perduodame informaciją į šabloną žodyno pavidale:
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # renderiname index.html, su duomenimis kintamąjame context
    return render(request, 'index.html', context=context)

def authors(request):
    authors = Author.objects.all()
    return render(request, 'authors.html', {'authors':authors})


def author(request, author_id):
    author = get_object_or_404(Author,id=author_id)
    return render(request, 'author.html', {'author':author})

from django.views import generic

class BookListView(generic.ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'book_list'
    #queryset = Book.objects.filter(title__icontains='n')

    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains = 'n')
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['blah'] = "test test"
    #     return context

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'