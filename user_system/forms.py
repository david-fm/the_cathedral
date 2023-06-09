from django import forms
from .models import UserPersonalized

class Publicate(forms.Form):
    title = forms.CharField(max_length=255, 
                            widget=forms.TextInput(
                                attrs={
                                    'placeholder': 'Title of new publication',
                                    'class':'entry-input',
                                    '@keyup.enter':'refs.new_publication.submit()'}
                            ), 
                            label='',
                            required=True)
    category = forms.CharField(max_length=255,
                                widget=forms.Select(
                                    attrs={
                                        'class':'entry-category',},
                                    choices=(
                                        ('', 'Select a category'),
                                        ('artificial-intelligence', 'Artificial Intelligence'),
                                        ('data-science', 'Data Science'),
                                        ('cybersecurity', 'Cybersecurity'),
                                        ('operating-systems', 'Operating Systems'),
                                    )
                                ),
                                label='',
                                required=True)

    

class UserConfig(forms.ModelForm):
    class Meta:
        model = UserPersonalized
        fields = ['image', 'first_name', 'last_name', 'email', 'website', 'biography']
        
        widgets = {
            'image': forms.FileInput(attrs={'class':'image-input'}),
            'first_name': forms.TextInput(attrs={'class':'input'}),
            'last_name': forms.TextInput(attrs={'class':'input'}),
            'website': forms.URLInput(attrs={'class':'input'}),
            'email': forms.EmailInput(attrs={'class':'input'}),
            'biography': forms.Textarea(attrs={'class':'text'}),
        }
        '''
        labels = {
            'image': 'Image',
            'first_name': 'Name',
            'last_name': 'Surname',
            'website': 'Website',
            'email': 'Email',
            'biography': 'Biography',
        }
        help_texts = {
            'image': 'Upload your image',
            'first_name': 'Enter your name',
            'last_name': 'Enter your surname',
            'website': 'Enter your website',
            'email': 'Enter your email',
            'biography': 'Enter your biography',
        }
        error_messages = {
            'image': {
                'max_length': "This writer's name is too long.",
            },
        }'''

class UserConfigPrivateData(forms.ModelForm):
    class Meta:
        model = UserPersonalized
        fields = ['gender', 'country', 'language']
        widgets = {
            # Select from male, female or other, if other is selected, a text input will appear
            'gender': forms.RadioSelect(attrs={'class':'input'}, choices=(
                ('m', 'male'),
                ('f', 'femlae'),
                ('o', 'other'),
            )),

            # Select from the european countries
            'country': forms.Select(attrs={'class':'input'}, choices=(
                ('', 'Select your country'),
                ('ES', 'Spain'),
                ('FR', 'France'),
                ('IT', 'Italy'),
                ('DE', 'Germany'),
                ('PT', 'Portugal'),
                ('UK', 'United Kingdom'),
                ('IE', 'Ireland'),
                ('BE', 'Belgium'),
                ('NL', 'Netherlands'),
                ('LU', 'Luxembourg'),
                ('DK', 'Denmark'),
                ('SE', 'Sweden'),
                ('FI', 'Finland'),
                ('AT', 'Austria'),
                ('GR', 'Greece'),
                ('PL', 'Poland'),
                ('CZ', 'Czech Republic'),
                ('SK', 'Slovakia'),
                ('HU', 'Hungary'),
                ('RO', 'Romania'),
                ('BG', 'Bulgaria'),
                ('HR', 'Croatia'),
                ('SI', 'Slovenia'),
                ('LT', 'Lithuania'),
                ('LV', 'Latvia'),
                ('EE', 'Estonia'),
                ('CY', 'Cyprus'),
                ('MT', 'Malta'),
            )),
            # Select from the 5th most spoken languages
            'language': forms.Select(attrs={'class':'input'}, choices=(
                ('', 'Select your language'),
                ('ZH', 'Chinese'),
                ('ES', 'Spanish'),
                ('EN', 'English'),
                ('HI', 'Hindi'),
                ('AR', 'Arabic'),
            ))
        }

class UserConfigPassword(forms.Form):
    password = forms.CharField(max_length=255, 
                            widget=forms.TextInput(
                                attrs={
                                    'placeholder': 'New password',
                                    'class':'input',
                                    'type':'password',}
                            ), 
                            label='')
    password_confirm = forms.CharField(max_length=255, 
                            widget=forms.TextInput(
                                attrs={
                                    'placeholder': 'Confirm new password',
                                    'class':'input',
                                    'type':'password',}
                            ), 
                            label='')