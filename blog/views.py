from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from .models import Post, Comment


class HomeView(TemplateView):
    template_name = 'home.html'


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'description']
    template_name = 'post_create.html'

    # adiciona o usuário
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PostCreateView, self).form_valid(form)

    # redireciona para o post
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post_list')

    # apenas o criador do post pode deleta-lo
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title', 'content', 'description']
    success_url = reverse_lazy('post_list')

    # apenas o criador do post pode edita-lo
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    context_object_name = 'comment'
    success_url = reverse_lazy('post_list')

    # apenas o criador do comentário pode deleta-lo
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = 'comment_update.html'
    fields = ['content']
    success_url = reverse_lazy('post_list')

    # apenas o criador do comentário pode deleta-lo
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user


@login_required(redirect_field_name='login')
def comment_create(request):
    '''
    View customizada para criar comentários.
    Obtém o comentário, o usuário, o url do post,
    para ser redirecionado, e seu id, para criar
    o comment no banco de dados, e finalmente
    redirecionar para o post.
    '''
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        post_url = request.META['HTTP_REFERER']
        # post_url.split('/') -> ['http:', '', 'localhost:8000', 'posts', '1', '']
        post_id = post_url.split('/')[-2]
        post = Post.objects.get(pk=post_id)

        new_comment = Comment(user=user, post=post, content=comment)
        new_comment.save()

        return redirect(post_url)
