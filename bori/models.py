from django.db import models
from pygments.lexers import get_lexer_by_name

class News(models.Model):
    url = models.CharField(max_length=500)
    name = models.CharField(max_length=100)

