# Description: This file contains an script to create a set of articles given a set of images in a folder.
import os
from .models import Publication, Block, BlockImage
from user_system.models import UserPersonalized
from django.contrib.auth.models import Group

IMAGES_DIR = ''

def create_articles():
    # Try to get the user named 'userTest' if it does not exist, create it and assign it group 'checkers'
    user = UserPersonalized.objects.filter(username='userTest').first()
    if user is None:
        user = UserPersonalized.objects.create_user(username='userTest',
                                                    password='userTest',
                                                    email='userTest@gmail.com')
        user.save()
        group_name = 'Checkers'
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
    
    # Do the same but with a user named 'userTest2' and group 'publishers'
    user2 = UserPersonalized.objects.filter(username='userTest2').first()
    if user2 is None:
        user2 = UserPersonalized.objects.create_user(username='userTest2',
                                                     password='userTest2',
                                                     email='userTest2@gmail.com')
        user2.save()
        group_name = 'Publishers'
        group = Group.objects.get(name=group_name)
        user2.groups.add(group)
    

    images = []
    for filename in os.listdir(IMAGES_DIR):
        if filename.endswith(".jpg"):
            images.append(filename)
                
    for index, image in enumerate(images):
        is_checked = user if index % 2 else None

        publication = Publication(publisher=user2, title=f'Example title {index}')
        publication.save()

        if is_checked:
            publication.checker.add(is_checked)
            publication.save()
        
        prev_block = Block.objects.get(publication=publication, next_block=None)
        block = Block(publication=publication, next_block=None)
        block.save()
        prev_block.next_block = block
        prev_block.save()

        block_image = BlockImage(block=block, file_path=image)
        block_image.save()
    


        
