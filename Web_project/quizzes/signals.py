from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import QuizResult, UserProfile
from .utils import update_leaderboard

@receiver(post_save, sender=QuizResult)
def update_user_score(sender, instance, created, **kwargs):
    if created:
        user_profile, created = UserProfile.objects.get_or_create(user=instance.user)
        user_profile.score += instance.score
        user_profile.save()
        update_leaderboard()

