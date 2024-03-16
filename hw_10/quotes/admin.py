from django.contrib import admin
from.models import Author, Quote, Tag


@admin.register(Author)
class  AuthorAdmin(admin.ModelAdmin):
    pass
    # list_display('id', 'fullname', 'born_date', 'born_location', )
