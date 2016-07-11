from django.shortcuts import render
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse
from .models import Author, Publication

def index(request):
    latest_pub_list = Publication.objects.order_by('-pub_date')[:5]

    template = loader.get_template('pubman/index.html')
    context = { 'latest_pub_list' : latest_pub_list, }

    return HttpResponse(template.render(context, request))

def authors_index(request, letter):
    if 'All' in letter:
        author_list = Author.objects.all()
    else:
        author_list = Author.objects.filter(last_name__startswith='%c' % letter)

    context = { 'author_list'       : author_list,
                'current_letter'    : letter,
    }
    return render(request, 'pubman/authors_index.html', context)

def author_detail(request, author_id):
    author = Author.objects.get(id=author_id)
    context = { 'author' : author,
                'author_pub_list' : author.publication_set.all(),
     }

    return render(request, 'pubman/author_detail.html', context)

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

    new_user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password2'])

    if new_user is not None:
        new_user.first_name = request.POST['first_name']
        new_user.last_name = request.POST['last_name']
        new_user.save()
        new_author = Author(first_name=new_user.first_name, last_name=new_user.last_name, user=new_user)

    new_author.save()

    return register(request, success=True)

def pub_index(request, success = False):
    if success == True:
        context = { 'success' : True }
    else:
        form1 = UserCreationForm()
        context = { 'pub_form' : form1 }

    context = {}
    return render(request, 'pubman/publications_index.html', context)

@login_required
def pub_create(request):
    new_pub = Publication(title=request.POST['title'])
    if new_pub is not None:
        new_pub.date_added = timezone.localtime(timezone.now())
        new_pub.pub_date = timezone.localtime(timezone.now() - timezone.timedelta(days=1))
        new_pub.save()

        try:
            author = Author.objects.get(first_name=request.POST['author_first_name'],
                                    last_name=request.POST['author_last_name'])
        except:
            author = Author(first_name=request.POST['author_first_name'],
                            last_name=request.POST['author_last_name'])

        author.publication_set.add(new_pub)

    return pub_index(request, success=True)

def publication_detail(request, pub_id):
    return HttpResponse("Publication details request with id %s" % pub_id)

def my_profile(request):
    return HttpResponse("MY PROFILE VIEW")
