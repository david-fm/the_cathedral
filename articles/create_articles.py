# Description: This file contains an script to create a set of articles given a set of images in a folder.
import os
from .models import Publication, Block, BlockImage

IMAGES_DIR = ''

def create_articles():
    images = []
    for filename in os.listdir(IMAGES_DIR):
        if filename.endswith(".jpg"):
            images.append(filename)
                
    for image in images:
        publication = Publication()
        publication.save()
        block = Block(publication=publication)
        block.save()
        block_image = BlockImage(block=block, file_path=image)
        block_image.save()

        
