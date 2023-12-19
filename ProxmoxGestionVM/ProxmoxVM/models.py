from django.db import models

#Modèle pour les OSs
class OperatingSystem(models.Model):
    name = models.CharField(max_length=100)
    name_os = models.CharField(max_length=100)
    def __str__(self):
        return self.name