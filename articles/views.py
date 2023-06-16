from typing import Any
from django import http
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
#from .models import Article
from django.views.generic.detail import DetailView
from django.views.generic import View
from .models import Publication
from .models import Publication, Font, Block, BlockAuthors, BlockImage, BlockText, BlockTitle, BlockDoi, BlockVideo, BlockQuiz, BlockReferences, BlockTable, Questions, Answer, Keywords, Comments
from .forms import UpdateTextBlock, UpdateTitleBlock, UpdateImageBlock, UpdateVideoBlock, UpdateAuthorsBlock, UpdateReferencesBlock, UpdateQuizBlock, UpdateQuestion, UpdateAnswer,  UpdateKeywordsBlock, UpdateComments
from django.forms import formset_factory, modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from user_system.models import UserPersonalized  # Requiere que el usuario inicie sesión
from django.views.decorators.csrf import csrf_protect
from django.http import Http404
from user_system.models import UserPersonalized
from django.contrib.auth.models import Group


#@permission_required('articles.is_checker', raise_exception=True)
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

def print_data_of_error_formsets(*formsets):
    for formset in formsets:
        if not formset.is_valid():
            print('error')
            print(formset.errors)
            print('Printing the formset')
            print(formset.as_table())

class ArticleDetailView(DetailView):
    model = Publication

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pub = self.object

        blocks = Block.objects.filter(publication=pub)
        blocks = order_blocks(blocks)
        keywords = Keywords.objects.get(publications=pub)
        
        context['blocks'] = blocks
        context['article_id'] = self.object.id
        context['keywords'] = keywords
        return context
    # Forbid the access if you are not the author
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('main:index')
        # if the user is not the author of the article, then return 404
        article = Publication.objects.get(id=self.kwargs['pk'])
        if article.publisher != request.user:
            return HttpResponseForbidden("Sorry, you are not the author of this article.")

        
        if not article.is_checked and request.user != article.publisher:
            raise HttpResponseForbidden("Sorry, this publication is not available for the users.")
        
        return super().dispatch(request, *args, **kwargs)

class ReviewView(DetailView):
    model = Publication
    template_name = 'articles/review.html'

    
    def dispatch(self, request, *args, **kwargs):
        print('hola')
        if not request.user.is_authenticated:
            return redirect('main:index')
        # if the user is not in the checker list of the article, then return http forbidden
        print(Publication.objects.get(id=self.kwargs['pk']).checks.all(), request.user)
        if not request.user in Publication.objects.get(id=self.kwargs['pk']).checks.all():
            return HttpResponseForbidden("Sorry, you are not the author of this article.")
        if not request.user.has_perm('user_system.is_checker'):
            return HttpResponseForbidden('You do not have permissions required')
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        
        blocks = Block.objects.filter(publication=self.object)
        blocks = order_blocks(blocks)
        keywords = Keywords.objects.get(publications=self.object)
        
        context['blocks'] = blocks
        context['article_id'] = self.object.id
        context['keywords'] = keywords
        return context
    def post(self, request, *args, **kwargs):
        # get the block
        block_id = request.POST.get('block_id')
        block = Block.objects.get(id=block_id)
        # get the text
        text = request.POST.get('text')
        # modify the comment
        comment = Comments.objects.get(block=block)
        comment.text = text
        comment.save()
        
        #context=super().get_context_data(**kwargs)
        return HttpResponse('')

class RejectAcceptArticleView(View):
    # Forbid the access if you are not the checker of the article
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('main:index')
        # if the user is not in the checker list of the article, then return http forbidden
        if not request.user in Publication.objects.get(id=self.kwargs['pk']).checks.all():
            return HttpResponseForbidden("Sorry, you are not the checker of this article.")
        if not request.user.has_perm('is_checker'):
            return HttpResponseForbidden('You do not have permissions required')
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        # get the article
        article_id = self.kwargs['pk']
        article = Publication.objects.get(id=article_id)
        # get the action
        action = request.POST.get('action')
        if action == 'accept':
            article.is_checked = True
            article.is_rejected = False
            article.is_published = False
            article.is_editable = False
            article.save()
            publisher = article.publisher
            # if the publisher has published more than 2 articles add it to the Checker group
            if Publication.objects.filter(publisher=publisher, is_published=True).count() >= 2:
                checker_group = Group.objects.get(name='Checker')
                publisher.groups.add(checker_group)
        elif action == 'reject':
            article.is_rejected = True
            article.is_published = False
            article.is_editable = True
            article.is_checked = False
            article.save()
        return redirect('user_system:reviewing_publication')

class PublishArticleView(View):
    # Forbid the access if you are not the publisher of the article
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('main:index')
        # if the user is not in the checker list of the article, then return http forbidden
        if not request.user == Publication.objects.get(id=self.kwargs['pk']).publisher:
            return HttpResponseForbidden("Sorry, you are not the author of this article.")
        if not request.user.has_perm('is_publisher'):
            return HttpResponseForbidden('You do not have permissions required')
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        # get the article
        article_id = request.POST.get('article_id')
        article = Publication.objects.get(id=article_id)
        # get the action
        action = request.POST.get('action')
        if action == 'publish':
            article.is_published = True
            article.is_editable = False
            article.is_checked = False
            article.is_rejected = False
            article.save()
        print('hola')
        return redirect('user_system:my_publications')

@login_required
def edit_view(request, article_id):
    
    # if it is not the author, return forbidden
    if request.user != Publication.objects.get(id=article_id).publisher:
        return HttpResponseForbidden("Sorry, you are not the author of this article.")
    # if the article is not editable, redirect to detail view
    if not Publication.objects.get(id=article_id).is_editable:
        return redirect('articles:detail', article_id)
    # By default comments wont be shown
    show_comments = False
    # if publication is rejected, show comments
    if Publication.objects.get(id=article_id).is_rejected:
        show_comments = True
    # take all the Block related to the publication and pass them to the template
    blocks = Block.objects.filter(publication=article_id)
    blocks = order_blocks(blocks)
    keywords = Keywords.objects.get(publications=article_id)
    # get which how many blocks of each type there are
    num_titles = BlockTitle.objects.filter(block__in=blocks).count()
    num_texts = BlockText.objects.filter(block__in=blocks).count()
    num_images = BlockImage.objects.filter(block__in=blocks).count()
    num_dois = BlockDoi.objects.filter(block__in=blocks).count()
    num_videos = BlockVideo.objects.filter(block__in=blocks).count()
    block_quizzes = BlockQuiz.objects.filter(block__in=blocks)
    num_quizzes = block_quizzes.count()
    
    questions = Questions.objects.filter(quiz_block__in=block_quizzes)
    num_questions = questions.count()
    answers = Answer.objects.filter(question__in=questions)
    num_answers = answers.count()

    num_references = BlockReferences.objects.filter(block__in=blocks).count()
    num_tables = BlockTable.objects.filter(block__in=blocks).count()
    num_authors = BlockAuthors.objects.filter(block__in=blocks).count()
    # TODO Implement keywords
    # create a formset for each type of block

    UpdateImageBlockSet = formset_factory(UpdateImageBlock, extra=num_images+1)
    UpdateTextBlockSet = formset_factory(UpdateTextBlock, extra=num_texts+1)
    UpdateTitleBlockSet = formset_factory(UpdateTitleBlock, extra=num_titles+1)
    UpdateVideoBlockSet = formset_factory(UpdateVideoBlock, extra=num_videos+1)
    UpdateAuthorsBlockSet = formset_factory(UpdateAuthorsBlock, extra=num_authors+1)
    UpdateReferencesBlockSet = formset_factory(UpdateReferencesBlock, extra=num_references+1)
    UpdateQuizBlockSet = formset_factory(UpdateQuizBlock, extra=num_quizzes+1)
    UpdateQuestionSet = formset_factory(UpdateQuestion, extra=num_questions+1)
    UpdateAnswerSet = formset_factory(UpdateAnswer, extra=num_answers+1)
    UpdateKeywordsBlockSet = formset_factory(UpdateKeywordsBlock, extra=1)
    text_formset = UpdateTextBlockSet(prefix='text')
    title_formset = UpdateTitleBlockSet(prefix='title')
    image_formset = UpdateImageBlockSet(prefix='image')
    video_formset = UpdateVideoBlockSet(prefix='video')
    authors_formset = UpdateAuthorsBlockSet(prefix='authors')
    references_formset = UpdateReferencesBlockSet(prefix='references')
    quizzes_formset = UpdateQuizBlockSet(prefix='quizzes')
    question_formset = UpdateQuestionSet(prefix='question')
    answer_formset = UpdateAnswerSet(prefix='answer')
    keywords_formset = UpdateKeywordsBlockSet(prefix='keywords')


    context = {'article_id': article_id, 'blocks': blocks, 'keywords':keywords,'text_formset': text_formset, 'title_formset': title_formset, 'image_formset':image_formset, 'video_formset':video_formset, 'authors_formset':authors_formset, 'references_formset':references_formset, 'quizzes_formset':quizzes_formset, 'question_formset':question_formset, 'answer_formset':answer_formset, 'keywords_formset':keywords_formset, 'show_comments':show_comments}
    return render(request, 'articles/editor.html', context=context)

def are_formsets_valids(*formsets):
    for formset in formsets:
        if not formset.is_valid():
            return False
    return True

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

    
def create_title_block(publication_id, form):
    '''Create a new block of type title and insert it after the block with id prev_block_id'''
    prev_block_id = form.cleaned_data['block_id']
    print(prev_block_id)
    prev_block = Block.objects.get(id=prev_block_id)
    # get publication
    publication = Publication.objects.get(id=publication_id)
    # Create the new block
    new_block = Block.objects.create(publication=publication)
    new_block.save()
    # Create the new title block
    new_title_block = BlockTitle.objects.create(block=new_block)
    new_title_block.save()
    # Update the previous block
    prev_block = Block.objects.get(id=prev_block_id)
    new_block.next_block = prev_block.next_block
    prev_block.next_block = new_block
    prev_block.save()
    new_block.save()


def del_title_block(form):
    print(form.cleaned_data)
    id_block = form.cleaned_data['block_id']
    block = Block.objects.get(id=id_block)
    block.blocktitle.delete()
    try:
        prev_block = Block.objects.get(next_block=block)
        prev_block.next_block = block.next_block
        prev_block.save()
    except:
        pass
    finally:
        block.delete()

def mod_title_block(form, files):

    print(form.cleaned_data)
    id_block = form.cleaned_data['block_id']

    title = form.cleaned_data['title']
    title = title.replace('<br>', '')
    block = Block.objects.get(id=id_block)
    block.blocktitle.title = title
    block.save()
    block.blocktitle.save()

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

def create_video_block(publication_id, form):
    '''Create a new block of type video and insert it after the block with id prev_block_id'''
    print(form.cleaned_data)
    prev_block_id = form.cleaned_data['block_id']
    # get publication
    publication = Publication.objects.get(id=publication_id)
    # Create the new block
    new_block = Block.objects.create(publication=publication)
    new_block.save()
    # Create the new video block
    new_video_block = BlockVideo.objects.create(block=new_block)
    new_video_block.save()
    # Update the previous block
    prev_block = Block.objects.get(id=prev_block_id)
    new_block.next_block = prev_block.next_block
    prev_block.next_block = new_block
    prev_block.save()
    new_block.save()

def del_video_block(form):
    print(form.cleaned_data)
    id_block = form.cleaned_data['block_id']
    block = Block.objects.get(id=id_block)
    block.blockvideo.delete()
    try:
        prev_block = Block.objects.get(next_block=block)
        prev_block.next_block = block.next_block
        prev_block.save()
    except:
        pass
    finally:
        block.delete()

def mod_video_block(form, files):
    id_block = form.cleaned_data['block_id']
    video = form.cleaned_data['url']
    video = video.split('/')[-1]
    video = f'https://www.youtube.com/embed/{video}'
    block = Block.objects.get(id=id_block)
    block.blockvideo.url = video
    block.save()
    block.blockvideo.save()

def create_authors_block(publication_id, form):
    '''Create a new block of type authors and insert it after the block with id prev_block_id'''
    print(form.cleaned_data)
    prev_block_id = form.cleaned_data['block_id']
    # get publication
    publication = Publication.objects.get(id=publication_id)
    # Create the new block
    new_block = Block.objects.create(publication=publication)
    new_block.save()
    # Create the new authors block
    new_authors_block = BlockAuthors.objects.create(block=new_block)
    new_authors_block.save()
    # Update the previous block
    prev_block = Block.objects.get(id=prev_block_id)
    new_block.next_block = prev_block.next_block
    prev_block.next_block = new_block
    prev_block.save()
    new_block.save()

def del_authors_block(form):
    print(form.cleaned_data)
    id_block = form.cleaned_data['block_id']
    block = Block.objects.get(id=id_block)
    block.blockauthors.delete()
    try:
        prev_block = Block.objects.get(next_block=block)
        prev_block.next_block = block.next_block
        prev_block.save()
    except:
        pass
    finally:
        block.delete()

def mod_authors_block(form, files):
    id_block = form.cleaned_data['block_id']
    authors = form.cleaned_data['authors']
    authors =  authors.split(",")
    authors = [author.strip() for author in authors]
    referenced_users = UserPersonalized.objects.filter(username__in=authors)

    block = Block.objects.get(id=id_block)
    block.blockauthors.authors.clear()
    for author in referenced_users:
        block.blockauthors.authors.add(author)
    block.save()
    block.blockauthors.save()

def create_references_block(publication_id, form):
    '''Create a new block of type references and insert it after the block with id prev_block_id'''
    print(form.cleaned_data)
    prev_block_id = form.cleaned_data['block_id']
    # get publication
    publication = Publication.objects.get(id=publication_id)
    # Create the new block
    new_block = Block.objects.create(publication=publication)
    new_block.save()
    # Create the new references block
    new_references_block = BlockReferences.objects.create(block=new_block)
    new_references_block.save()
    # Update the previous block
    prev_block = Block.objects.get(id=prev_block_id)
    new_block.next_block = prev_block.next_block
    prev_block.next_block = new_block
    prev_block.save()
    new_block.save()

def del_references_block(form):
    print(form.cleaned_data)
    id_block = form.cleaned_data['block_id']
    block = Block.objects.get(id=id_block)
    block.blockreferences.delete()
    try:
        prev_block = Block.objects.get(next_block=block)
        prev_block.next_block = block.next_block
        prev_block.save()
    except:
        pass
    finally:
        block.delete()

def mod_references_block(form, files):
    id_block = form.cleaned_data['block_id']
    title = form.cleaned_data['title']
    title = title.replace('<br>', '')
    url = form.cleaned_data['url']
    block = Block.objects.get(id=id_block)
    block.blockreferences.title = title
    print(url)
    if url != 'Link to article':
        print(url)
        block.blockreferences.url = url
    block.save()
    block.blockreferences.save()

def mod_keywords_block(publication_id, form):
    keywords = form.cleaned_data['keywords']
    print(keywords)
    # get 
    actual_keywords = Keywords.objects.get(publications=publication_id)
    actual_keywords.keyword = keywords
    print(actual_keywords.keyword)
    actual_keywords.save()

def create_quiz_block(publication_id, form):
    '''Create a new block of type quiz and insert it after the block with id prev_block_id'''
    print(form.cleaned_data)
    prev_block_id = form.cleaned_data['block_id']
    # get publication
    publication = Publication.objects.get(id=publication_id)
    # Create the new block
    new_block = Block.objects.create(publication=publication)
    new_block.save()
    # Create the new quizzes block
    new_quiz_block = BlockQuiz.objects.create(block=new_block, name = "Write the name of the quiz")
    new_quiz_block.save()


    question = Questions.objects.create(quiz_block = new_quiz_block, question="Write here a question")
    question.save()

    answer = Answer.objects.create(question=question, answer="Write here an answer")
    answer.save()
    
    # Update the previous block
    prev_block = Block.objects.get(id=prev_block_id)
    new_block.next_block = prev_block.next_block
    prev_block.next_block = new_block
    prev_block.save()
    new_block.save()

def del_quiz_block(form):
    print(form.cleaned_data)
    id_block = form.cleaned_data['block_id']
    block = Block.objects.get(id=id_block)
    block.blockquiz.delete()
    # TODO: Delate all questions and asnwer from the block
    try:
        prev_block = Block.objects.get(next_block=block)
        prev_block.next_block = block.next_block
        prev_block.save()
    except:
        pass
    finally:
        block.delete()

def mod_quiz_block(form, files):

    print(form.cleaned_data)
    id_block = form.cleaned_data['block_id']

    name = form.cleaned_data['name']
    block = Block.objects.get(id=id_block)
    block.blockquiz.name = name

    block.save()
    block.blockquiz.save()

def create_question(publication_id, form):
    '''Create a new question and insert it in the quiz'''
    print(form.cleaned_data)
    
    # get Quiz block

    id_question = form.cleaned_data['block_id']
    question = Questions.objects.get(id=id_question)

    quiz_block = question.quiz_block

    question = Questions.objects.create(quiz_block=quiz_block)
    question.save()

    answer = Answer.objects.create(question=question, answer="Write here an answer")
    answer.save()

    

def del_question(form):
    print(form.cleaned_data)
    
    id_question = form.cleaned_data['block_id']
    
    question = Questions.objects.get(id=id_question)
   
    question.delete()
   

def mod_question(form, files):

    print(form.cleaned_data)
    id_question = form.cleaned_data['block_id']

    question = Questions.objects.get(id=id_question)

    question_text = form.cleaned_data['question']

    question.question = question_text
    question.save()


def create_answer(publication_id, form):
    '''Create a new answer and insert it in the quiz'''
    print(form.cleaned_data)
    
    # get Answer
    id_answer = form.cleaned_data['block_id']
    answer = Answer.objects.get(id=id_answer)

    question = answer.question

    answer = Answer.objects.create(question=question)
    
    answer.save()

    
def del_answer(form):
    print(form.cleaned_data)
    
    id_answer = form.cleaned_data['block_id']
    
    answer = Answer.objects.get(id=id_answer)
   
    answer.delete()
   

def mod_answer(form, files):

    print(form.cleaned_data)
    id_answer = form.cleaned_data['block_id']

    answer = Answer.objects.get(id=id_answer)

    answer_text = form.cleaned_data['answer']
    is_correct = form.cleaned_data['is_correct']

    answer.answer = answer_text
    answer.is_correct = is_correct
    answer.save()

    
dict_block_type_to_functions = {
    'T': {'create': create_text_block, 'delete': del_text_block, 'modify': mod_text_block},
    'Ti': {'create': create_title_block, 'delete': del_title_block, 'modify':mod_title_block},
    'I': {'create': create_image_block, 'delete': del_image_block, 'modify': mod_image_block},
    #'D': {'create': create_doi_block, 'delete': del_doi_block, 'modify': mod_doi_block},
    'V': {'create': create_video_block, 'delete': del_video_block, 'modify': mod_video_block},
    'Q': {'create': create_quiz_block, 'delete': del_quiz_block, 'modify': mod_quiz_block},
    'Qq': {'create': create_question, 'delete': del_question, 'modify': mod_question},
    'Qa': {'create': create_answer, 'delete': del_answer, 'modify': mod_answer},
    'R': {'create': create_references_block, 'delete': del_references_block, 'modify': mod_references_block},
    'A': {'create': create_authors_block, 'delete': del_authors_block, 'modify': mod_authors_block},
    #'B': {'create': create_table_block, 'delete': del_table_block, 'modify': mod_table_block},
}

@login_required
def save(request, article_id):
    print('save')
    text_formset = formset_factory(UpdateTextBlock)
    text_formset = text_formset(request.POST, prefix='text')
    image_formset = formset_factory(UpdateImageBlock)
    title_formset = formset_factory(UpdateTitleBlock)
    title_formset = title_formset(request.POST, prefix='title')
    image_formset = image_formset(request.POST, request.FILES, prefix='image')
    video_formset = formset_factory(UpdateVideoBlock)
    video_formset = video_formset(request.POST, prefix='video')
    authors_formset = formset_factory(UpdateAuthorsBlock)
    authors_formset = authors_formset(request.POST, prefix='authors')
    references_formset = formset_factory(UpdateReferencesBlock)
    references_formset = references_formset(request.POST, prefix='references')
    quizzes_formset = formset_factory(UpdateQuizBlock)
    quizzes_formset = quizzes_formset(request.POST, prefix='quizzes')

    question_formset = formset_factory(UpdateQuestion)
    question_formset = question_formset(request.POST, prefix='question')
    answer_formset = formset_factory(UpdateAnswer)
    answer_formset = answer_formset(request.POST, prefix='answer')

    keywords_formset = formset_factory(UpdateKeywordsBlock)
    keywords_form = keywords_formset(request.POST, prefix='keywords')

    if keywords_form.is_valid():
        print('keywords valid')
        status = keywords_form[0].cleaned_data['status']
        if status == 'M':
            print('modifying keywords')
            mod_keywords_block(article_id, keywords_form[0])
    else:
        print('keywords invalid')
        print(keywords_form.errors)
        print(keywords_form.as_table())

    # print forms as html
    '''
    print(authors_formset.as_table())
    print(text_formset.as_table())
    print(image_formset.as_table())
    print(video_formset.as_table())
    '''
    if are_formsets_valids(text_formset, image_formset, video_formset, authors_formset, references_formset, title_formset, quizzes_formset, question_formset, answer_formset):
        print('valid')
        list_of_forms_and_types = [
            (text_formset, 'T'),
            (image_formset, 'I'),
            (video_formset, 'V'),
            (authors_formset, 'A'),
            (references_formset, 'R'),
            (title_formset, 'Ti'),
            (quizzes_formset, 'Q'),
            (question_formset, 'Qq'),
            (answer_formset, 'Qa'),
            #...
        ]
        for formset, block_type in list_of_forms_and_types:
            print('block_type', block_type)
            for form in formset:
                status = form.cleaned_data['status']
                if status == 'D':
                    # delete the block
                    print('delete')
                    dict_block_type_to_functions[block_type]['delete'](form)

                elif status == 'C':
                    # create a new block
                    print('create')
                    dict_block_type_to_functions[block_type]['create'](article_id, form)
                elif status == 'M':
                    # modify the block
                    print('modify')
                    dict_block_type_to_functions[block_type]['modify'](form, request.FILES)
    else:
        print_data_of_error_formsets(text_formset, image_formset, video_formset, authors_formset, references_formset, title_formset, quizzes_formset, question_formset, answer_formset)
    return redirect('articles:edit', article_id=article_id)






# TODO Make that create_block also saves the data of the form
# Search may have in mind
# - blocks to be created
# - blocks to be deleted
# - blocks to be saved