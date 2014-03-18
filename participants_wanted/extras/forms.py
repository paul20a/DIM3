from django import forms
from extras.models import Role, Production, Director, Actor
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

class ProductionForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text=('Please enter the title.'))
    genre = forms.CharField(max_length=128, help_text=mark_safe('<br />Please enter the genre.'))
    description = forms.CharField(max_length=128, help_text=mark_safe('<br />Please enter a description.'))
    cost = forms.CharField(max_length=128, help_text=mark_safe('<br />Please enter a cost.'))
    openingDate = forms.CharField(max_length=128, help_text=mark_safe('<br />Please enter closing date.'))
    closingDate = forms.CharField(max_length=128, help_text=mark_safe('<br />Please enter opening date.'))

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Production
        fields = ('title', 'genre', 'description', 'openingDate','closingDate', 'cost',)

class RoleForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text='Please enter a role name.')
    gender = forms.CharField(max_length=128, help_text=mark_safe('<br />Please enter a gender.'))
    roleType = forms.CharField(max_length=128, help_text=mark_safe('<br />Please enter a role type.'))
    description = forms.CharField(max_length=128, help_text=mark_safe('<br />Please enter a description.'))

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Role

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        fields = ('name', 'gender', 'roleType', 'description',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url is not empty and doesn't start with 'http://', prepend 'http://'.
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',)

class DirectorProfileForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = ('agency',) # Can add more fields for register

class ActorProfileForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ('dateOfBirth', 'height', 'weight', 'hairColour','eyeColour' ,'gender', 'rating', 'picture') # Can add more fields for register
