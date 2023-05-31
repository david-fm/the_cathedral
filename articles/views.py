from django.shortcuts import redirect, render
from django.http import HttpResponse
#from .models import Article
from .models import Publication
from .models import Publication, Font, Block, BlockAuthors, BlockImage, BlockText, BlockTitle, BlockDoi, BlockVideo, BlockQuiz, BlockReferences, BlockTable, Questions, Answer, Keywords
from .forms import UpdateTextBlock, UpdateImageBlock
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


@login_required
def edit_view(request, article_id):
    # take all the Block related to the publication and pass them to the template
    blocks = Block.objects.filter(publication=article_id)
    blocks = order_blocks(blocks)
    # get which how many blocks of each type there are
    num_titles = BlockTitle.objects.filter(block__in=blocks).count()
    num_texts = BlockText.objects.filter(block__in=blocks).count()
    num_images = BlockImage.objects.filter(block__in=blocks).count()
    num_dois = BlockDoi.objects.filter(block__in=blocks).count()
    num_videos = BlockVideo.objects.filter(block__in=blocks).count()
    num_quizzes = BlockQuiz.objects.filter(block__in=blocks).count()
    num_references = BlockReferences.objects.filter(block__in=blocks).count()
    num_tables = BlockTable.objects.filter(block__in=blocks).count()
    num_authors = BlockAuthors.objects.filter(block__in=blocks).count()
    # TODO Implement keywords
    # create a formset for each type of block

    UpdateImageBlockSet = formset_factory(UpdateImageBlock, extra=num_images+1)
    UpdateTextBlockSet = formset_factory(UpdateTextBlock, extra=len(blocks)+1)
    text_formset = UpdateTextBlockSet(prefix='text')
    image_formset = UpdateImageBlockSet(prefix='image')


    context = {'article_id': article_id, 'blocks': blocks, 'text_formset': text_formset, 'image_formset':image_formset}
    return render(request, 'articles/editor.html', context=context)

def are_formsets_valids(*formsets):
    for formset in formsets:
        if not formset.is_valid():
            return False
    return True

def print_data_of_error_formsets(*formsets):
    for formset in formsets:
        if not formset.is_valid():
            print('error')
            print(formset.errors)
            print('Printing the formset')
            print(formset.as_table())

@login_required
def save(request, article_id):
    print('save')
    text_formset = formset_factory(UpdateTextBlock)
    text_formset = text_formset(request.POST, prefix='text')
    image_formset = formset_factory(UpdateImageBlock)
    image_formset = image_formset(request.POST, request.FILES, prefix='image')
    # print forms as html
    #print(forms.as_table())
    if are_formsets_valids(text_formset, image_formset):
        for form in text_formset:
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
        print_data_of_error_formsets(text_formset, image_formset)
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

def image_block(publication_id, prev_block_id):
    '''Create a new block of type image and insert it after the block with id prev_block_id'''
    # get publication
    publication = Publication.objects.get(id=publication_id)
    # Create the new block
    new_block = Block.objects.create(publication=publication)
    new_block.save()
    # Create the new image block
    new_image_block = BlockImage.objects.create(block=new_block)
    new_image_block.save()
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