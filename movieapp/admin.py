from django.contrib import admin

from .models import Person, Movie, Role, Cast, Genre

# Register your models here.

admin.site.register(Role)
admin.site.register(Person)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Cast)
