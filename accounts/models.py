from django.db import models
from django.contrib.auth.models import User
# importing django signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timesince import timesince
from django.utils import timezone
from datetime import timedelta, datetime


#profile picture location
def profile_image_path_location(instance, filename):
    # get todays date YYYY-MM-DD format
    today_date = datetime.now().strftime('%Y-%m-%d')
    #return the upload path
    return "profile/%s/%s/%s" % (instance.user.username, today_date, filename)
   



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(upload_to=profile_image_path_location, blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

    @property
    def profile_picture_url(self):
        try:
            image = self.profile_picture.url
        except:
            image = "https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909__340.png"
        return image
    
    # @property
    # def full_name(self):
    #     first_name = self.user.first_name
    #     last_name = self.user.last_name
    #     if first_name and last_name:
    #         return f"{first_name} {last_name}"
    #     return self.user.username
    @property
    def full_name(self):
        name = self.user.get_full_name()
        if name:
            return name
        return self.user.get_username()
    
    # @property
    # def date_joined(self):
    #     return timesince(self.user.date_joined)

    @property
    def date_joined(self):
        time_diff = timezone.now() - self.user.date_joined
        if time_diff <= timedelta(days=2):
            return timesince(self.user.date_joined) + " ago"
        else:
            return self.user.date_joined.strftime('%d %b')



# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, **kwargs):
    # if a user already exist and has no profile, create
    Profile.objects.get_or_create(user=instance)


