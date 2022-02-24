from django.db import models
from django.contrib.auth import get_user_model

class Turma(models.Model):
    nome = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    inicio = models.DateField()
    fim = models.DateField()
    matriculas = models.ManyToManyField(get_user_model())