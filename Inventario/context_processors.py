from .models import Profile
from django.utils import timezone
from datetime import timedelta

def user_profile(request):
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)
        now = timezone.now()
        online = (now - profile.last_seen) < timedelta(minutes=2)
        return {'user_profile': profile, 'is_online': online}
    return {} 