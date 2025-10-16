from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False)
    # NO PASSWORD IN THE USER CLASS FOR NOW.
    # I'd much prefer that we just create a User db object when registering a new user.
    # If we end up needing to still store that password here, so be it.

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    player_id = models.AutoField(primary_key=True)
