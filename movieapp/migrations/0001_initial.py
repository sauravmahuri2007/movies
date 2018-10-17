# Generated by Django 2.1.2 on 2018-10-16 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dtm', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'cast',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=30, unique=True)),
                ('description', models.CharField(default=None, max_length=45, null=True)),
                ('created_dtm', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'genre',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100)),
                ('plot', models.TextField(default='', max_length=200, null=True)),
                ('release_date', models.DateTimeField(default=None, null=True)),
                ('run_time', models.IntegerField(default=0, null=True)),
                ('rating', models.DecimalField(decimal_places=1, default=None, max_digits=3, null=True)),
                ('created_dtm', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'movie',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50)),
                ('gender', models.CharField(default=None, max_length=5, null=True)),
                ('dob', models.DateTimeField(default=None, null=True)),
                ('created_dtm', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'person',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=50, unique=True)),
                ('description', models.CharField(default=None, max_length=45, null=True)),
                ('created_dtm', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'role',
            },
        ),
        migrations.AddField(
            model_name='person',
            name='roles',
            field=models.ManyToManyField(to='movieapp.Role'),
        ),
        migrations.AddField(
            model_name='movie',
            name='director',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='movieapp.Person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(to='movieapp.Genre'),
        ),
        migrations.AddField(
            model_name='cast',
            name='movie_id',
            field=models.ForeignKey(db_column='movie_id', on_delete=django.db.models.deletion.DO_NOTHING, to='movieapp.Movie'),
        ),
        migrations.AddField(
            model_name='cast',
            name='person_id',
            field=models.ForeignKey(db_column='person_id', on_delete=django.db.models.deletion.DO_NOTHING, to='movieapp.Person'),
        ),
    ]