from .models import UserProfile
from django.core.mail import send_mail
from django.conf import settings

def send_rank_notification(email, username, new_rank):
    subject = "Вас обігнали в рейтингу"
    message = (
        f"Шановний {username},\n\n"
        f"Вас обігнали в рейтингу! Ваш новий рейтинг: {new_rank}.\n"
        "Поверніться на сайт та продовжуйте набирати бали, щоб відновити свою позицію!"
    )
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

def update_leaderboard():
    leaderboard = UserProfile.objects.order_by('-score')
    for i, user_profile in enumerate(leaderboard):
        old_rank = user_profile.rank
        new_rank = i + 1
        if old_rank and old_rank != new_rank:
            # Если ранг изменился, отправляем уведомление
            send_rank_notification(
                user_profile.user.email,
                user_profile.user.username,
                new_rank
            )
        user_profile.rank = new_rank
        user_profile.save()
