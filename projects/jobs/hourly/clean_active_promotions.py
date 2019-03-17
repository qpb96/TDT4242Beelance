from django_extensions.management.jobs import BaseJob

class Job(BaseJob):
    help = "Active Promotion (db) clean up"

    def execute(self):
        from projects.models import ActivePromotion
        from django.utils import timezone

        active_promotions = ActivePromotion.objects.all()
        now = timezone.now()
        for active_promotion in active_promotions:
            if active_promotion.is_expired():
                active_promotion.delete()
                