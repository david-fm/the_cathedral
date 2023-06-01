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

def del_text_block(form):
    print('del_text_block')
    print(form.cleaned_data)
    id_block = form.cleaned_data['block_id']
    block = Block.objects.get(id=id_block)
    text_block = BlockText.objects.get(block=block)
    try:
        prev_block = Block.objects.get(next_block=block)
        prev_block.next_block = block.next_block
        prev_block.save()
    except:
        pass
    finally:
        text_block.delete()
        block.delete()

def mod_text_block(form, files):

    print(form.cleaned_data)
    id_block = form.cleaned_data['block_id']
    print(f'mod_text_block {id_block}')

    text = form.cleaned_data['text']
    block = Block.objects.get(id=id_block)
    block.blocktext.text = text
    block.save()
    block.blocktext.save()

def create_text_block(publication_id, form):
    '''Create a new block of type text and insert it after the block with id prev_block_id'''
    prev_block_id = form.cleaned_data['block_id']
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

def create_image_block(publication_id, form):
    '''Create a new block of type image and insert it after the block with id prev_block_id'''
    prev_block_id = form.cleaned_data['block_id']
    print(prev_block_id)
    prev_block = Block.objects.get(id=prev_block_id)
    # get publication
    publication = Publication.objects.get(id=publication_id)
    # Create the new block
    new_block = Block.objects.create(publication=publication)
    new_block.save()
    # Create the new image block
    new_image_block = BlockImage.objects.create(block=new_block)
    new_image_block.save()
    # Update the previous block
    
    
    new_block.next_block = prev_block.next_block
    prev_block.next_block = new_block
    prev_block.save()
    new_block.save()

def del_image_block(form):
    print(form.cleaned_data)
    id_block = form.cleaned_data['block_id']
    block = Block.objects.get(id=id_block)
    block.blockimage.delete()
    try:
        prev_block = Block.objects.get(next_block=block)
        prev_block.next_block = block.next_block
        prev_block.save()
    except:
        pass
    finally:
        block.delete()

def mod_image_block(form, files):
    
    id_block = form.cleaned_data['block_id']
    image = form.cleaned_data['file']
    block = Block.objects.get(id=id_block)
    block.blockimage.file_path = image
    block.save()
    block.blockimage.save()
    


dict_block_type_to_functions = {
    'T': {'create': create_text_block, 'delete': del_text_block, 'modify': mod_text_block},
    'I': {'create': create_image_block, 'delete': del_image_block, 'modify': mod_image_block},
    #'D': {'create': create_doi_block, 'delete': del_doi_block, 'modify': mod_doi_block},
    #'V': {'create': create_video_block, 'delete': del_video_block, 'modify': mod_video_block},
    #'Q': {'create': create_quiz_block, 'delete': del_quiz_block, 'modify': mod_quiz_block},
    #'R': {'create': create_references_block, 'delete': del_references_block, 'modify': mod_references_block},
    #'A': {'create': create_authors_block, 'delete': del_authors_block, 'modify': mod_authors_block},
    #'K': {'create': create_keywords_block, 'delete': del_keywords_block, 'modify': mod_keywords_block},
    #'B': {'create': create_table_block, 'delete': del_table_block, 'modify': mod_table_block},
}

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
        list_of_forms_and_types = [
            (text_formset, 'T'),
            (image_formset, 'I'),
            #...
        ]
        for formset, block_type in list_of_forms_and_types:
            for form in formset:
                status = form.cleaned_data['status']
                if status == 'D':
                    # delete the block
                    dict_block_type_to_functions[block_type]['delete'](form)

                elif status == 'C':
                    # create a new block
                    dict_block_type_to_functions[block_type]['create'](article_id, form)
                elif status == 'M':
                    # modify the block
                    dict_block_type_to_functions[block_type]['modify'](form, request.FILES)
    else:
        print_data_of_error_formsets(text_formset, image_formset)
    return redirect('articles:edit', article_id=article_id)






# TODO Make that create_block also saves the data of the form
# Search may have in mind
# - blocks to be created
# - blocks to be deleted
# - blocks to be saved