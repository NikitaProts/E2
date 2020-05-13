from django.db import models

# Create your models here.

class Mail(models.Model):
    address = models.EmailField()
    subject = models.CharField(max_length=128)
    content = models.TextField()
    send_time = models.DateTimeField(verbose_name="send time")
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} to {self.address} on {self.send_time}"
