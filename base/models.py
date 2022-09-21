from django.db import models


# Create your models here.

# This will be a user model in the future
class Image(models.Model):
    title = models.CharField(max_length=200)
    # uploads to MEDIA_ROOT/images
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title
