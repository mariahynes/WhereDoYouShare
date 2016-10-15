from django.shortcuts import render
from .forms import ContactForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect

# function to return the index.html template
def get_index(request):
    return render(request, 'index.html')

# function to render a basic contact form
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'maria@databasis.ie'),['maria.m.hynes@gmail.com'],
            )
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm(
            initial={'subject': 'Where | do you Share? | Question'}
        )
    return render(request, 'contact_form.html', {'form':form})