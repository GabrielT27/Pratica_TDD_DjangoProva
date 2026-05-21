from django.db import models
from django.contrib.auth.models import User

class LinkModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=150)
    url = models.URLField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo