from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField('auth.Group', related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_set', blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.email if self.email else 'S/N'
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)




class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    date_birth = models.DateField('Data de nascimento', null=True, blank=True)
    phone = models.CharField('Telefone', max_length=200, null=True, blank=True)
    # bio = models.CharField(max_length=200, null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=CustomUser, dispatch_uid="create_profile")
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# class ContactUs(models.Model):
#     full_name = models.CharField(max_length=200, null=True, blank=True)
#     email = models.CharField(max_length=200, null=True, blank=True)
#     phone = models.CharField('Telefone', max_length=200, null=True, blank=True)
#     subject = models.CharField(max_length=200, null=True, blank=True)
#     message = models.TextField(null=True, blank=True)

#     class Meta:
#         verbose_name = 'Contato'
#         verbose_name_plural = 'Contatos'

#     def __str__(self):
#         return self.full_name