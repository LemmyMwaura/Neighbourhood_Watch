from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User

class Neighbourhood(models.Model):
    name = models.CharField(max_length=150)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

    def create_neighbourhood(self):
        self.save()

    def delete_neighbourhood(self):
        self.delete()
  
    def update_neighbourhood(self):
        self.save()

    def update_occupants():
        return Neighbourhood.objects.all().count()

    @classmethod
    def find_neighbourhood(cls,neigborhood_id):
        return cls.objects.get(id=neigborhood_id)


class Profile(models.Model):
    user_profile = models.OneToOneField(User, related_name='currentuser', on_delete=models.CASCADE)
    bio = models.TextField()
    location = models.CharField(max_length=150, blank=True)
    users_neighbourhood = models.ForeignKey(Neighbourhood, related_name='members', on_delete=models.DO_NOTHING, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.user_profile.username

class Post(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    hood = models.ForeignKey(Neighbourhood, related_name='posts', on_delete=models.CASCADE)
    message = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.message[:50]

    def create_post(self):
        self.save()

    def delete_post(self):
        self.delete()

class Business(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    email = models.EmailField(blank=True)
    business_number = PhoneField(blank=True, help_text='Enter your Business\' Phone Number, ext(extention) is optional')
    users_name = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Neighbourhood_bsns = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return f'{self.name} business'

    def create_business(self):
        self.save()
  
    def delete_business(self):
        self.delete()

    def update_business(self):
        self.save()

    @classmethod
    def find_business(cls,business_id):
        return cls.objects.get(id=business_id)