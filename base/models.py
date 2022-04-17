from django.db import models
from django.contrib.auth.models import User

class Neighbourhood(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
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
  
    def update_neighbourhood():
        pass

    def update_occupants():
        pass

    @classmethod
    def find_neighbourhood(cls,neigborhood_id):
        return cls.objects.filter(id=neigborhood_id)


class Profile(models.Model):
    user_profile = models.OneToOneField(User, related_name='currentuser', on_delete=models.CASCADE)
    bio = models.TextField()
    users_neighbourhood = models.ForeignKey(Neighbourhood, related_name='members', on_delete=models.DO_NOTHING, blank=True)
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
    # comments = models.ForeignKey('Comment',related_name='comments', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.message[:50]

    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()

class Business(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
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
  
    def update_business(self):
        self.delete()

    @classmethod
    def find_business(cls,business_id):
        cls.objects.filter(id=business_id)