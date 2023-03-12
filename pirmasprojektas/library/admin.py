from .models import Author, Genre, Book, BookInstance
from django.contrib import admin

class AuthorAdmin(admin.ModelAdmin):
    list_display =("last_name", "first_name", "display_books")

class BookInstanceInLine(admin.TabularInline):
    model = BookInstance
    extra = 0
    readonly_fields = ("id",)
    can_delete = False


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "display_genre")
    inlines = [BookInstanceInLine]

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ("book", "status", "due_back")
    list_filter = ("status", "due_back")

    fieldsets = (("General", {"fields": ("id", "book")}), ("Availability", {"fields": ("status","due_back")}))

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance, BookInstanceAdmin)