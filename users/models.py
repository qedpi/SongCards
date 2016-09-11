from django.contrib.auth.models import Permission, User
from django.db import models

'''
class UserProfile(models.Model):
    #friends = models.ManyToManyField(User, related_name='friends')


    #friends = models.ManyToManyField('self', null=True)

    friends = models.ManyToManyField('self', null=True)
'''

class FriendshipManager(models.Manager):

    def friends_for_user(self, user):
        return self.filter(from_user=user).select_related(depth=1)

    def friends_of_user(self, user):
        return self.filter(to_user=user).select_related(depth=1)

    def remove_from_to(self, user1, user2):
        self.filter(from_user=user1, to_user=user2).delete()

class Friendship(models.Model):
    to_user = models.ForeignKey(User, related_name="friends")
    from_user = models.ForeignKey(User)

    objects = FriendshipManager()

    class Meta:
        unique_together=('to_user', 'from_user',)

#def friends_for(user):
        # return Friendship.objects.friends_for_user(user)