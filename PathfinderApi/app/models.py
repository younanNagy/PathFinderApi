from django.db import models
import uuid

class Node(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    child = models.OneToOneField('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='parent')

    def __str__(self):
        return self.name