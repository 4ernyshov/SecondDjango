from django.db import models

LANGS = (
    ("py", "Python"),
    ("cpp", "C++"),
    ("html", "HTML"),
    ("js", "JavaScript"),
    ("java", "Java")
)

class Snippet(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=30, choices=LANGS)
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(auto_now=True)
