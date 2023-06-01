from django import forms


class UpdateTextBlock(forms.Form):
    text = forms.CharField(max_length=3500, required=False, empty_value='', widget=forms.Textarea(), label='')
    block_id = forms.IntegerField(label='', required=False)
    status = forms.CharField(max_length=1, widget=forms.HiddenInput(), label='')

    # TODO
    #font_size = forms.FloatField()
    #font = forms.ManyToManyField(Font, blank=True)

class UpdateImageBlock(forms.Form):
    file = forms.ImageField(label='', required=False)
    block_id = forms.IntegerField(label='', required=False)
    status = forms.CharField(max_length=1, widget=forms.HiddenInput(), label='')
