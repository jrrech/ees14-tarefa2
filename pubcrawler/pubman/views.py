from django.shortcuts import render
from django.template import loader

from django.http import HttpResponse
from .models import Author, Publication

def index(request):
	latest_pub_list = Publication.objects.order_by('-pub_date')[:5]

	template = loader.get_template('pubman/index.html')
	context = { 'latest_pub_list' : latest_pub_list, }

	if not latest_pub_list:
		output = "There are no publications yet!"
	else:
	    output = ', '.join([pub.title for pub in latest_pub_list])

	return HttpResponse(template.render(context, request))

def authors_index(request):
	context = {}
	return render(request, 'pubman/authors_index.html', context)

def author_detail(request, author_id):
	return HttpResponse("Author details request with id %d" % author_id)

def pub_index(request):
	context = {}
	return render(request, 'pubman/publications_index.html', context)

def publication_detail(request, pub_id):
	return HttpResponse("Publication details request with id %s" % pub_id)

def my_profile(request):
	return HttpResponse("MY PROFILE VIEW")
