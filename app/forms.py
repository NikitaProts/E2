from threading import Thread
from time import sleep
from datetime import timedelta
from django import forms
from django.core.mail import send_mail
from django.utils import timezone
from app.models import Mail
from E2 import settings


def send_thread(address, subject, content, sleep_time, mail_instance):
    sleep(sleep_time)
    send_mail(subject=subject,
              message=content,
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=[address])
    mail_instance.sent = True
    mail_instance.save()
    

class MailForm(forms.Form):
    
    address = forms.EmailField()
    subject = forms.CharField(widget=forms.TextInput)
    content = forms.CharField(widget=forms.Textarea)
    send_time = forms.IntegerField(min_value=1, help_text='seconds to sending')
    
    def send_mail(self):        
        mail = Mail.objects.create(address=self.cleaned_data["address"],
                                   subject=self.cleaned_data["subject"],
                                   content=self.cleaned_data["content"],
                                   send_time=timezone.now()+timedelta(seconds=int(self.cleaned_data["send_time"])),
                                   sent=False)

        t = Thread(target=send_thread, args=(self.cleaned_data["address"],
                                             self.cleaned_data["subject"],
                                             self.cleaned_data["content"],
                                             int(self.cleaned_data["send_time"]),
                                             mail), 
                                             daemon=True)
                
        t.start()
        