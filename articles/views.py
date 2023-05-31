from django.shortcuts import redirect, render
from django.http import HttpResponse
#from .models import Article
from .models import Publication
from .models import Publication, Font, Block, BlockAuthors, BlockImage, BlockText, BlockTitle, BlockDoi, BlockVideo, BlockQuiz, BlockReferences, BlockTable, Questions, Answer, Keywords
from .forms import UpdateTextBlock
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseForbidden

@login_required  # Requiere que el usuario inicie sesión
#@permission_required('articles.is_checker', raise_exception=True)
def my_view(request):
    if not request.user.has_perm('articles.is_checker'):
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

    return HttpResponse("¡Hola, usuario con permiso!")

def detail(request, article_id):
    return HttpResponse("You're looking at article %s." % article_id)

def order_blocks(blocks):
    '''
        Given a list of blocks, order them by their next_block_id
    '''
    ordered_blocks = []
    # find the last block
    for block in blocks:
        if block.next_block is None:
            ordered_blocks.append(block)
            break
    
    # find the previous block
    while len(ordered_blocks) < len(blocks):
        for block in blocks:
            if block.next_block == ordered_blocks[-1]:
                ordered_blocks.append(block)
                break
    ordered_blocks.reverse()
    return ordered_blocks

def edit_view(request, article_id):
    # take all the Block related to the publication and pass them to the template
    blocks = Block.objects.filter(publication=article_id)
    blocks = order_blocks(blocks)
    # add a form per each block
    UpdateTextBlockSet = formset_factory(UpdateTextBlock, extra=len(blocks)+1)
    formset = UpdateTextBlockSet()
    context = {'article_id': article_id, 'blocks': blocks, 'forms': formset}
    return render(request, 'articles/editor.html', context=context)

def save(request, article_id):

    forms = formset_factory(UpdateTextBlock)
    forms = forms(request.POST)
    # print forms as html
    print(forms.as_table())
    if forms.is_valid():
        for form in forms:
            status = form.cleaned_data['status']
            if status == 'D':
                # delete the block
                id_block = form.cleaned_data['block_id']
                block = Block.objects.get(id=id_block)
                try:
                    prev_block = Block.objects.get(next_block=block)
                    prev_block.next_block = block.next_block
                    prev_block.save()
                except:
                    pass
                finally:
                    block.delete()

            elif status == 'C':
                # create a new block
                text_block(article_id, form.cleaned_data['block_id'])
            elif status == 'M':
                # modify the block
                id_block = form.cleaned_data['block_id']
                block = Block.objects.get(id=id_block)
                block.blocktext.text = form.cleaned_data['text']
                block.save()
                block.blocktext.save()
    else:
        print(forms.errors)
    return redirect('articles:edit', article_id=article_id)

def text_block(publication_id, prev_block_id):
    '''Create a new block of type text and insert it after the block with id prev_block_id'''
    # get publication
    publication = Publication.objects.get(id=publication_id)
    # Create the new block
    new_block = Block.objects.create(publication=publication)
    new_block.save()
    # Create the new text block
    new_text_block = BlockText.objects.create(block=new_block)
    new_text_block.save()
    # Update the previous block
    prev_block = Block.objects.get(id=prev_block_id)
    new_block.next_block = prev_block.next_block
    prev_block.next_block = new_block
    prev_block.save()
    new_block.save()




# TODO Make that create_block also saves the data of the form
# Search may have in mind
# - blocks to be created
# - blocks to be deleted
# - blocks to be saved