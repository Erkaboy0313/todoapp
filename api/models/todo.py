from tortoise.models import Model
from tortoise.fields import IntField,BooleanField,CharField,ForeignKeyField


class List(Model):
    id = IntField(pk=True)
    name = CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Task(Model):
    id = IntField(pk=True)
    list = ForeignKeyField("models.List",related_name='related_list')
    task = CharField(max_length=100)
    done = BooleanField(default=False)