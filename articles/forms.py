from django import forms

'''
class BlockText(Block):
    text = models.CharField(max_length=3500)
    font_size = models.FloatField()
    font = models.ManyToManyField(Font, blank=True)
'''

class UpdateTextBlock(forms.Form):
    text = forms.CharField(max_length=3500, required=False, empty_value='')
    block_id = forms.IntegerField()

    # TODO
    #font_size = forms.FloatField()
    #font = forms.ManyToManyField(Font, blank=True)
