# -*- coding: utf-8 -*-

from django.db import models

class Role(models.Model):
    title = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.CharField(max_length=45, default=None, null=True)
    created_dtm = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'role'

    def __str__(self):
        return self.title


class Person(models.Model):
    name = models.CharField(max_length=50, null=False, db_index=True)
    roles = models.ManyToManyField(Role)
    gender = models.CharField(max_length=5, null=True, default=None)
    dob = models.DateTimeField(default=None, null=True)
    created_dtm = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'person'

    def __str__(self):
        return self.name


class Genre(models.Model):
    title = models.CharField(max_length=30, unique=True, db_index=True)
    description = models.CharField(max_length=45, default=None, null=True)
    created_dtm = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'genre'

    def __str__(self):
        return self.title


class Movie(models.Model):
    title = models.CharField(max_length=100, null=False, db_index=True)
    plot = models.TextField(max_length=200, null=True, default='')
    release_date = models.DateTimeField(default=None, null=True)
    run_time = models.IntegerField(default=0, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, default=None)
    genres = models.ManyToManyField(Genre)
    director = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    author = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    created_dtm = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'movie'

    def __str__(self):
        return self.title


class Cast(models.Model):
    movie_id = models.ForeignKey(Movie, db_column='movie_id', on_delete=models.DO_NOTHING)
    person_id = models.ForeignKey(Person, db_column='person_id', on_delete=models.DO_NOTHING)
    created_dtm = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cast'

    def __str__(self):
        return '{0} - {1}'.format(self.movie_id.title, self.person_id.name)