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
