from django.db import models

class ToDoList(models.Model):
    # Python instance variables can have different values across multiple instances of a class.
    # Class variables share the same value among all instances of the class.
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self):
        return self.text

class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)

    access_token = models.CharField(max_length=500)
    expires_in = models.IntegerField()
    expires_at = models.FloatField()
    refresh_token = models.CharField(max_length=500)

    def __str__(self):
        return f"""
            access_token: {self.access_token},
            expires_in: {self.expires_in},
            expires_at: {self.expires_at},
            refresh_token: {self.refresh_token},
        """