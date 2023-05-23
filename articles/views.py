from django.shortcuts import redirect, render
from django.http import HttpResponse
#from .models import Article
from .models import Publication
from .models import Publication, Font, BlockAuthors, BlockImage, BlockText, BlockTitle, BlockDoi, BlockVideo, BlockQuiz, BlockReferences, BlockTable, Questions, Answer, Keywords
from .forms import UpdateTextBlock
from django.forms import formset_factory



def detail(request, article_id):
    return HttpResponse("You're looking at article %s." % article_id)

def order_blocks(blocks):
    '''
        Given a list of blocks, order them by their next_block_id
    '''
    ordered_blocks = []
    # find the last block
    for block in blocks:
        if block.next_block_id is None:
            ordered_blocks.append(block)
            break
    # find the previous block
    while len(ordered_blocks) < len(blocks):
        for block in blocks:
            if block.next_block_id == ordered_blocks[-1]:
                ordered_blocks.append(block)
                break
    ordered_blocks.reverse()
    return ordered_blocks

def edit_view(request, article_id):
    # take all the BlockText related to the publication and pass them to the template
    text_blocks = BlockText.objects.filter(publication_id=article_id)
    text_blocks = order_blocks(text_blocks)
    # add a form per each block
    UpdateTextBlockSet = formset_factory(UpdateTextBlock, extra=len(text_blocks))
    formset = UpdateTextBlockSet()
    context = {'article_id': article_id, 'text_blocks': text_blocks, 'forms': formset}
    return render(request, 'articles/editor.html', context=context)

def save(request, article_id):

    forms = formset_factory(UpdateTextBlock)
    forms = forms(request.POST)
    if forms.is_valid():
        for form in forms:
            print(form)
            id_block = form.cleaned_data['block_id']
            text_block = BlockText.objects.get(id=id_block)
            text_block.text = form.cleaned_data['text']
            text_block.save()
    return redirect('articles:edit', article_id=article_id)

def create_block(request, publication_id, prev_block_id):
    prev_block = BlockText.objects.get(id=prev_block_id)
    publication = Publication.objects.get(id=publication_id)
    new_block = BlockText(publication_id=publication)
    new_block.save()
    new_block.next_block_id = prev_block.next_block_id
    prev_block.next_block_id = new_block
    new_block.save()
    prev_block.save()
    return redirect('articles:edit', article_id=publication_id)

