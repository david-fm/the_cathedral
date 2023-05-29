from django import forms

class Publicate(forms.Form):
    title = forms.CharField(max_length=255, 
                            widget=forms.TextInput(
                                attrs={
                                    'placeholder': 'New entry',
                                    'class':'entry-input',
                                    '@keyup.enter':'refs.new_publication.submit()'}
                            ), 
                            label='')