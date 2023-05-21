from django.contrib import admin

# Register your models here.

from .models import Publication, Font, BlockAuthors, BlockImage, BlockText, BlockTitle, BlockDoi, BlockVideo, BlockQuiz, BlockReferences, BlockTable

admin.site.register(Publication)
admin.site.register(Font)
admin.site.register(BlockAuthors)
admin.site.register(BlockImage)
admin.site.register(BlockText)
admin.site.register(BlockTitle)
admin.site.register(BlockDoi)
admin.site.register(BlockVideo)
admin.site.register(BlockQuiz)
admin.site.register(BlockReferences)
admin.site.register(BlockTable)
