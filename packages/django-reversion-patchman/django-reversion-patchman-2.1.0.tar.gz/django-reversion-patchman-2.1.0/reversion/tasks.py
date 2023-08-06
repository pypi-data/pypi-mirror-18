from celery import shared_task
from celery.utils.log import task_logger
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.utils import timezone
from reversion.models import Revision, Version

@shared_task(ignore_result=True)
def prune():
    revisions = Revision.objects.filter(date_created__lt = timezone.now() \
                                                       - relativedelta(days=settings.AUDIT_LOG_RETENTION_DAYS)) \
                                .values_list('pk')
    Version.objects.filter(revision__in=revisions).delete()
    Revision.objects.filter(pk__in=revisions).delete()
