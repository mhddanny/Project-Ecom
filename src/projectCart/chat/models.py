from django.db import models
from accounts.models import Account

# Create your models here.
class Message(models.Model):
    body = models.TextField()
    send_by = models.CharField(max_length=255)
    created_at= models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Account, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.send_by

    def last_10_messages():
        return Message.objects.order_by('-created_at').all()[:10]
    
class Room(models.Model):
    WAITING = 'waiting'
    ACTIVE = 'active'
    CLOSED = 'closed'

    CHOICES_STATUS = {
        (WAITING, 'Waiting'),
        (ACTIVE, 'Active'),
        (CLOSED, 'Closed'),
    }

    uuid = models.CharField(max_length=255)
    client = models.CharField(max_length=255)
    agent = models.ForeignKey(Account, related_name='rooms', blank=True, null=True, on_delete=models.SET_NULL)
    messages = models.ManyToManyField(Message, blank=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=WAITING)
    created_at= models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.client}' '-' f'{self.uuid}'
