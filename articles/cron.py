from .models import Publication
from user_system.models import UserPersonalized
from django.contrib.auth.models import Group
from django_cron import CronJobBase, Schedule
import random
 # checkers can't have a publication assigned if they are already checking one publication and it is not rejected or accepted
def checking_publication(checker):
            
    checked_publications = Publication.objects.filter(checks=checker)
            
    for pub in checked_publications:
        if  not pub.is_rejected and not pub.is_checked :
            return True
    return None
class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  # every minute

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'articles.my_cron_job'  # a unique code

    def do(self):

        checked_users = UserPersonalized.objects.filter(checks__isnull=False).distinct()  # Accede a las publicaciones que están en el campo 'checks'
        checked_publications = Publication.objects.filter(checks__in=checked_users).distinct()
        
        pubs_no_checkers = Publication.objects.filter(is_checked=False, is_published = True).exclude(id__in=checked_publications)
        print("NO chequeadas")
        print(pubs_no_checkers)
        print("checked users")
        print(checked_users)
        print("chequedas")
        print(checked_publications)
        print("checkers")
        # checkers can't have a publication assigned if they are already checking one publication and it is not rejected or accepted
        available_checkers = UserPersonalized.objects.filter(available=True)
        for checker in available_checkers:
            if checking_publication(checker) is not None:
                available_checkers = available_checkers.exclude(pk=checker.pk)

        print(available_checkers)
        for pub in pubs_no_checkers:
            checkers = available_checkers.exclude(pk=pub.publisher.id) # exclude pubs of the checker
            random_checker = random.choice(checkers)
            pub.checks.add(random_checker)