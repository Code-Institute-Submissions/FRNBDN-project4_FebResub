from django.shortcuts import render
from .models import *
from django.views import generic


class Feed(generic.ListView):
    model = Post
    queryset = Post.objects.filter(listed=True).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 5


# def home_page_view(request):
#     context = {}
#     feed = Post.objects.filter(listed=True).order_by('-created_on')
#     context['feed'] = feed

#     return render(request, 'index.html', context)