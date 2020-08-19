from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    """ Custom User is extended by default Django User """
    photo = models.ImageField(upload_to='image\photo', blank=True, default='icon\placeholder-profile.jpg')

    def get_absolute_url(self):
        return reverse("profile_url", kwargs={'pk': self.pk})

    def get_status(self):
        """Show red or green circle-status for mini avatar"""
        return 'bg-success' if self.is_active else 'bg-danger'
    
    def get_avatar_url(self):
        """Returns URL of image"""
        return self.photo.url

    def avatar_tag(self):
        """ Rendering mini avatar """
        return mark_safe(
            '<a href="%s"> <div class="card-parent-mini"><div class="card-avatar-mini"><img  class="card-avatar-mini-img" src="%s" ><span class="card-avatar-status-mini %s"></span></div></div>' % (
            self.get_absolute_url(),  self.get_avatar_url(), self.get_status()))

    def save(self, *args, **kwargs):
        """ Set default image if the user doesn't have a photo"""
        if self.photo == '':
           self.photo = 'icon\placeholder-profile.png'
        super(User, self).save(*args, **kwargs)
