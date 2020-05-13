from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import FormView
from app.models import Mail
from app.forms import MailForm

# Create your views here.


class CreateMailView(FormView):
    template_name = "send_form.html"
    form_class = MailForm
    success_url = "/mail/"

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


class MailList(ListView):
    model = Mail
    template_name = "mail_list.html"
    queryset = Mail.objects.order_by("-send_time")[:10]