from django import forms
from .models import BlockTitle, BlockDoi, BlockVideo, BlockQuiz, BlockReferences, BlockTable, BlockAuthors, Questions, Answer, Comments


class UpdateTextBlock(forms.Form):
    text = forms.CharField(max_length=3500, required=False, empty_value='', widget=forms.Textarea(), label='')
    block_id = forms.IntegerField(label='', required=False)
    status = forms.CharField(max_length=1, widget=forms.HiddenInput(), label='')

    # TODO
    #font_size = forms.FloatField()
    #font = forms.ManyToManyField(Font, blank=True)

class UpdateTitleBlock(forms.ModelForm):
    block_id = forms.IntegerField(label='', required=False)
    status = forms.CharField(max_length=1, widget=forms.HiddenInput(), label='')
    class Meta:
        model = BlockTitle
        fields = ['title']
        labels = {
            'title': '',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'TITLE'}),
        }



class UpdateImageBlock(forms.Form):
    file = forms.ImageField(label='', required=False)
    block_id = forms.IntegerField(label='', required=False)
    status = forms.CharField(max_length=1, widget=forms.HiddenInput(), label='')

class UpdateVideoBlock(forms.ModelForm):
    block_id = forms.IntegerField(label='', required=False)
    status = forms.CharField(max_length=1, widget=forms.HiddenInput(), label='')
    class Meta:
        model = BlockVideo
        fields = ['url']
        labels = {
            'url': '',
        }
        widgets = {
            'url': forms.TextInput(attrs={'placeholder': 'URL'}),
        }

class UpdateAuthorsBlock(forms.Form):
    block_id = forms.IntegerField(label='', required=False)
    status = forms.CharField(max_length=1, widget=forms.HiddenInput(), label='')
    authors = forms.CharField(max_length=255, required=False, empty_value='', label='')

class UpdateReferencesBlock(forms.ModelForm):
    block_id = forms.IntegerField(label='', required=False)
    status = forms.CharField(max_length=1, widget=forms.HiddenInput(), label='')
    class Meta:
        model = BlockReferences
        fields = ['title', 'url']
        labels = {
            'title': '',
            'url': '',
        }
        widgets = {
            'url': forms.TextInput(attrs={'placeholder': 'URL'}),
        }

class UpdateQuizBlock(forms.ModelForm):
    block_id = forms.IntegerField(label='', required=False)
    status = forms.CharField(max_length=1, widget=forms.HiddenInput(), label='')
    class Meta:
        model = BlockQuiz
        fields = ['name']
        labels = {
            'name': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'NAME'}),
        }

class UpdateQuestion(forms.ModelForm):
    block_id = forms.IntegerField(label='', required=False)
    status = forms.CharField(max_length=1, widget=forms.HiddenInput(), label='')
    class Meta:
        model = Questions
        fields = ['question']
        labels = {
            'question': '',
        }
        widgets = {
            'question': forms.TextInput(attrs={'placeholder': 'QUESTION'}),
        }

class UpdateAnswer(forms.ModelForm):
    block_id = forms.IntegerField(label='', required=False)
    status = forms.CharField(max_length=1, widget=forms.HiddenInput(), label='')
    class Meta:
        model = Answer
        fields = ['answer', 'is_correct']
        labels = {
            'answer': '',
            'is_correct': '',
        }
        widgets = {
            'answer': forms.TextInput(attrs={'placeholder': 'ANSWER'}),
            'is_correct': forms.CheckboxInput(),
            
        }

"""
class UpdateTableBlock(forms.ModelForm):
    block_id = forms.IntegerField(label='', required=False)
    status = forms.CharField(max_length=1, widget=forms.HiddenInput(), label='')
    class Meta:
        model = BlockTable
        fields = ['text', 'font_size', 'font']
        labels = {
            'text': '',
            'font_size': '',
            'font': '',
        }
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'TEXT'}),
            'font_size': forms.IntegerField(attrs={'placeholder': 'SIZE'})
            'font': forms.ChoiceField(),
        }
"""
class UpdateKeywordsBlock(forms.Form):
    status = forms.CharField(max_length=1, widget=forms.HiddenInput(), label='')
    keywords = forms.CharField(max_length=255, required=False, empty_value='', label='')

class UpdateComments(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text', 'block']
        labels = {
            'text': '',
            'block': '',
        }
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'placeholder': 'Insert your comment here...',
                    'x-data':"{ resize: () => { $el.style.height = '5px'; $el.style.height = $el.scrollHeight + 'px' } }",
                    'x-init':'resize()',
                    '@input':'resize();'}),
        }