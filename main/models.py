from django.db import models
from django.urls import reverse 

class Location(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='locations/')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('location_detail', args=[str(self.id)])
