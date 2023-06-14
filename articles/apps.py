from django.apps import AppConfig
# Create a signal for post_save of Blocks model to create a Comments model associated with the Block.


class ArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'articles'

    def ready(self):
        import articles.signals