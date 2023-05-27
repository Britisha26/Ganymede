from .models import Agent,AgentRating,AgentReview
from django import forms
from phone_field import PhoneFormField,PhoneWidget


class AgentForm(forms.ModelForm):
    name=forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={
        'placeholder':'Eg. Jack Sparrow',
        'class':'restroform'
        })
    )
    
    vehile_license=forms.CharField(
        label='Vehile License Number',
        widget=forms.TextInput(attrs={
        'placeholder':'Eg. TN 00 EG 1234',
        'class':'restroform'
        })
    )

    aadhar=forms.IntegerField(
        label='Aadhar Number',
        widget=forms.TextInput(attrs={
        'class':'restroform'   
        })
    )

    pic=forms.ImageField(
        label="Profile Picture",
        widget=forms.ClearableFileInput(attrs={
        'class':'restroform'
        })
    )

    phone=PhoneFormField(
        label="Phone No",
        widget=PhoneWidget(attrs={
        'class':'restroform'
        })
    )

    emergency_contact=PhoneFormField(
        label="Emergency Contact Number",
        widget=PhoneWidget(attrs={
        'class':'restroform'
        })
    )

    email=forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
        'class':'restroform'
        })
    )

    previous_workplace=forms.CharField(
        label="Previous Workplace",
        widget=forms.Textarea(attrs={
        'placeholder':'Eg. Infosys',
        'class':'restroform'
        })
    )
    
    address=forms.CharField(label="Address",
        widget=forms.Textarea(attrs={
        'placeholder':'Eg 26 Maple Drive',
        'rows':'3',
        'cols':'6',
        'class':'restroform'
        })
    )
    

    def clean_phone(self):
        return self.cleaned_data['phone'] or None
    
    def clean_email(self):
        return self.cleaned_data['email'] or None
    
    class Meta:
        model=Agent
        fields=['name','aadhar','pic','phone','email','vehile_license','emergency_contact','address','previous_workplace']