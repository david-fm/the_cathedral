"""
    This module contains the forms used in the articles edition.
"""
from django import forms
from .models import BlockTitle, BlockDoi, BlockVideo, BlockQuiz, BlockReferences, BlockTable, BlockAuthors


class UpdateTextBlock(forms.Form):
    """
    :class: 'UpdateTextBlock'

    UpdateTextBlockis a class that represents a form to update the text of a text block.
    """
    text = forms.CharField(max_length=3500, required=False, empty_value='', widget=forms.Textarea(), label='')
    block_id = forms.IntegerField(label='', required=False)
    status = forms.CharField(max_length=1, widget=forms.HiddenInput(), label='')

    # TODO
    #font_size = forms.FloatField()
    #font = forms.ManyToManyField(Font, blank=True)

class UpdateTitleBlock(forms.ModelForm):
    """
    :class: 'UpdateTitleBlock'
    
    UpdateTitleBlockis a class that represents a form to update the title of a title block.
    """
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
    """
    :class: 'UpdateImageBlock'

    UpdateImageBlockis a class that represents a form to update the image of a image block.
    """
    file = forms.ImageField(label='', required=False)
    block_id = forms.IntegerField(label='', required=False)
    status = forms.CharField(max_length=1, widget=forms.HiddenInput(), label='')

class UpdateVideoBlock(forms.ModelForm):
    """
    :class: 'UpdateVideoBlock'

    UpdateVideoBlockis a class that represents a form to update the video of a video block.
    """
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
    """
    :class: 'UpdateAuthorsBlock'

    UpdateAuthorsBlockis a class that represents a form to update the authors of a authors block.
    """

    block_id = forms.IntegerField(label='', required=False)
    status = forms.CharField(max_length=1, widget=forms.HiddenInput(), label='')
    authors = forms.CharField(max_length=255, required=False, empty_value='', label='')

class UpdateReferencesBlock(forms.ModelForm):
    """
    :class: 'UpdateReferencesBlock'

    UpdateReferencesBlockis a class that represents a form to update the references of a references block.
    """
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
    """
    :class: 'UpdateKeywordsBlock'

    UpdateKeywordsBlockis a class that represents a form to update the keywords of a keywords block.
    """
    status = forms.CharField(max_length=1, widget=forms.HiddenInput(), label='')
    keywords = forms.CharField(max_length=255, required=False, empty_value='', label='')