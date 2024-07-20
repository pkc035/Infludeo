from django.db import models

class PhotoCard(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='photo_cards/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name