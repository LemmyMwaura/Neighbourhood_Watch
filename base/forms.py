from django.forms import EmailField, EmailInput, ModelForm, TextInput, Textarea, CharField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Business, Profile, Post
from phone_field.forms import PhoneWidget
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = [ 'user','hood','updated', 'created']
        widgets = {
            'message' : Textarea(attrs={'class':'post-form-message', 'rows':4, 'cols':35}),
        }

class BusinessForm(ModelForm):
    class Meta:
        model = Business
        fields = '__all__'
        exclude = ['updated','created','users_name','Neighbourhood_bsns']
        widgets = {
            'name':TextInput(attrs={'class':'business-name'}),
            'description' : Textarea(attrs={'class':'business-description', 'rows':4, 'cols':35}),
            'email': EmailInput(attrs={'class':'business-email'}),
            'business_number': PhoneWidget(attrs={'class':'business-number'}),
        }

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['updated','created','user_profile','users_neighbourhood']
        widgets = {
            'bio': Textarea(attrs={'class':'profile-form-bio','rows':4, 'cols':35}),
            'location': TextInput(attrs={'class':'profile-form-location'})
        }

class UserRegistrationForm(UserCreationForm):
    first_name = CharField(max_length=50, widget=TextInput(attrs={'class':'new-user-firstname'}))
    last_name = CharField(max_length=50, widget=TextInput(attrs={'class':'new-user-lastname'}))
    email = EmailField(widget=EmailInput(attrs={'class':'new-user-email'}))
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs={'class' : 'new-user-username'}
        self.fields['password1'].widget.attrs={'class' : 'new-user-password'}
        self.fields['password2'].widget.attrs={'class': 'new-user-confirm-password'}