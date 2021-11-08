from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, PostCategory, Category
from .filters import PostFilter
from .forms import PostForm


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'news/index.html'

    def get_context_data(self, **kwargs):
        # получили весь контекст из класса-родителя
        context = super().get_context_data(**kwargs)
        # добавили новую контекстную переменную is_no t_premium
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context
    # Чтобы ответить на вопрос, есть ли пользователь в группе, мы заходим в переменную запроса self.request
#     Из этой переменной мы можем вытащить текущего пользователя. В поле groups хранятся все группы,
#     в которых он состоит. Далее мы применяем фильтр к этим группам и ищем ту самую, имя которой premium.
#     После чего проверяем, есть ли какие-то значения в отфильтрованном списке.
#     Метод exists() вернет True, если группа premium в списке групп пользователя найдена, иначе — False.
#     А нам нужно получить наоборот — True, если пользователь не находится в этой группе,
#     поэтому добавляем отрицание not, и возвращаем контекст обратно.


class PostList(ListView):
    model = Post
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    # queryset = Post.objects.order_by('-id')
    ordering = ['-id']
    paginate_by = 10


class PostsSearch(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'posts_search'
    ordering = ['-time_of_creation']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


# дженерик для отображения деталей объекта
class PostDetailView(DetailView):
    template_name = 'news/post_detail.html'
    queryset = Post.objects.all()


# дженерик для создания объекта.
class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'news/post_add.html'
    form_class = PostForm


# дженерик для редактирования объекта
class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'news/post_add.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'


