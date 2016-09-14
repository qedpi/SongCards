from django.contrib.auth.models import Permission, User
from django.db import models

'''
class UserProfile(models.Model):
    #friends = models.ManyToManyField(User, related_name='friends')


    #friends = models.ManyToManyField('self', null=True)

    friends = models.ManyToManyField('self', null=True)
'''

class FriendshipManager(models.Manager):

    # I share with
    def friends_for_user(self, user):
        return self.filter(from_user=user)#.prefetch_related("user_set")

    # They share with me
    def friends_of_user(self, user):
        return self.filter(to_user=user)#.prefetch_related("user_set")

    def remove_from_to(self, user1, user2):
        self.filter(from_user=user1, to_user=user2).delete()

    def is_friend_either(self, user1, user2):
        #return len(self.friends_for_user(user=user1)) + len(self.friends_of_user(user=user1)) > 0
        return self.filter(from_user=user1, to_user=user2).exists() \
               or self.filter(from_user=user2, to_user=user1).exists()


class Friendship(models.Model):
    to_user = models.ForeignKey(User, related_name="friends")
    from_user = models.ForeignKey(User, related_name="reverse_friends")

    objects = FriendshipManager()

    class Meta:
        unique_together=('to_user', 'from_user',)

    def __str__(self):
        return self.from_user.username + ' shares with ' + self.to_user.username
#def friends_for(user):
        # return Friendship.objects.friends_for_user(user)