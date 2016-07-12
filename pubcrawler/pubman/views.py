from django.shortcuts import render
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse
from .models import Author, Publication
from django.views.static import serve
from django.contrib.auth.decorators import login_required

def favico(request):
    filepath = '../icon.jpg'
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

def index(request):
    latest_pub_list = Publication.objects.order_by('-pub_date')[:5]

    context = { 'latest_pub_list' : latest_pub_list, }

    return render(request, 'pubman/index.html', context)

###################################################################################################

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
    success = False
    if request.POST['password1'] != request.POST['password2']:
        return HttpResponse(" THE PASSWORDS DO NOT MATCH!")

    try:
        User.objects.get(username=request.POST['username'])
    except:
        new_user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password2'])
        new_user.first_name = request.POST['first_name']
        new_user.last_name = request.POST['last_name']

        if new_user is not None and request.POST.get('is_author'):
            new_user.save()
            new_author = Author(first_name=new_user.first_name, last_name=new_user.last_name, user=new_user)
            new_author.save()

        success = True

    return register(request, success)

###################################################################################################

def pub_index(request, success = False):
    context = { 'pub_list' : Publication.objects.all() }

    return render(request, 'pubman/publications_index.html', context)

@login_required(login_url='/login/')
def pub_add(request, success = False):
    if success == True:
        context = { 'success' : True }
    else:
        form1 = UserCreationForm()
        context = { 'pub_form' : form1 }

    return render(request, 'pubman/add_publication.html', context)

@login_required(login_url='/login/')
def pub_create(request):
    success = False

    new_pub = Publication(title=request.POST['title'])

    if new_pub is not None:
        new_pub.date_added = timezone.localtime(timezone.now())
        new_pub.pub_date = timezone.localtime(timezone.now() - timezone.timedelta(days=1))
        new_pub.keywords = request.POST['keywords']
        new_pub.save()

        try:
            author = Author.objects.get(first_name=request.POST['author_first_name'],
                                    last_name=request.POST['author_last_name'])

        except:
            author = Author(first_name=request.POST['author_first_name'],
                            last_name=request.POST['author_last_name'])

            author.save()

        author.publication_set.add(new_pub)
        success = True

    return pub_add(request, success)

def publication_detail(request, pub_id):
    pub = Publication.objects.get(id=pub_id)

    if pub is None:
        return HttpResponse(" No publication with id %s" % pub_id)

    authors = pub.authors.all()
    for author in authors:
        author.last_name = author.last_name.upper()

    context = { 'pub' : pub,
                'authors' : authors }

    return render(request, 'pubman/publication_detail.html', context)

###################################################################################################


