from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView,CreateView, UpdateView, DeleteView
from .models import Post

def home(request):
    Content = {
        'posts':Post.objects.all()
    }
    return render(request,'blog/home.html',Content)

# It will return a list in a newly created post
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_of_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_of_posted')

# It will return the detail of the post

# Ye LoginRequiredMixin method hume ek functionality provide krti hai ki agr koi user logout hai 
# to sbse pehle use login krwana pdega fir hi wo blog create kr skta hai

# It will create a new post.
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'desc']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        # redirect('blog-home')

class PostDetailView(DetailView):
    model = Post


# It will update our post.
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'desc']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        # redirect('blog-home')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# This will delete the current logged in user of post
class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
def contact(request):
    return render(request,'blog/contact.html')
