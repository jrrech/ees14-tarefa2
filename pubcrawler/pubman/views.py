from django.shortcuts import render
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.http import HttpResponse
from .models import Author, Publication

def index(request):
	latest_pub_list = Publication.objects.order_by('-pub_date')[:5]

	template = loader.get_template('pubman/index.html')
	context = { 'latest_pub_list' : latest_pub_list, }

	return HttpResponse(template.render(context, request))

def authors_index(request, letter):
    author_list = Author.objects.filter(last_name__startswith='%c' % letter)

    context = { 'author_list'       : author_list,
                'current_letter'    : letter,
    }
    return render(request, 'pubman/authors_index.html', context)

def author_detail(request, author_id):
	return HttpResponse("Author details request with id %s" % author_id)

def register(request, success = False):
    if success == True:
        context = { 'success' : True }
    else:
        form1 = UserCreationForm()
        context = { 'creation_form' : form1 }

    return render(request, 'pubman/register.html', context)

def author_create(request):
    if request.POST['password1'] != request.POST['password2']:
        return HttpResponse(" THE PASSWORDS DO NOT MATCH!")

    User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password2'])

    return register(request, success=True)

def pub_index(request):
	context = {}
	return render(request, 'pubman/publications_index.html', context)

def publication_detail(request, pub_id):
	return HttpResponse("Publication details request with id %s" % pub_id)

def my_profile(request):
	return HttpResponse("MY PROFILE VIEW")
