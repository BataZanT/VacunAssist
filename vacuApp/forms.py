
from django import forms


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
                'id': 'loginEmail',
                'type': 'text',
                'class': 'form-control'
            })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'loginPassword',
            'type': 'password',
            'class': 'form-control',
        })
       )
    token = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'loginToken',
            'type': 'text',
            'class': 'form-control'
         })
    )
 