from django.shortcuts import render, redirect, get_object_or_404
from .models import Articles, Comment
from .forms import ArticlesForm, CommentForm
from django.views.generic import DetailView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
 

def news_home(request):
    news = Articles.objects.order_by('-date')
    return render(request, 'news/news_home.html', {'news': news})

class NewsDetailView(DetailView):
    model = Articles
    template_name = 'news/details_view.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            # Создание нового комментария
            comment = Comment(
                article=self.object,
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                content=form.cleaned_data['content']
            )
            comment.save()
            return redirect(self.object.get_absolute_url())
        return self.get(request, *args, **kwargs)

class NewsUpdateView(UpdateView):
    model = Articles
    template_name = 'news/create.html'

    form_class = ArticlesForm

class NewsDeleteView(DeleteView):
    model = Articles
    success_url = '/news/'
    template_name = 'news/news-delete.html'




def create(request):
    error = ''
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

        else:
            error = 'Форма не верна'


    form = ArticlesForm()

    data = {
        'form': form,
        'error': error

    }

    return render(request, 'news/create.html', data)

def register(request, article_id=None):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if article_id:
                return redirect('news-detail', pk=article_id)
            return redirect('news_home')
    else:
        form = UserCreationForm()
    
    # Передаем article_id в контекст шаблона
    return render(request, 'registration/register.html', {'form': form, 'article_id': article_id})



class CustomLoginView(LoginView):
    def get_success_url(self):
        # Здесь перенаправляем на нужный URL после успешного входа
        return self.request.GET.get('next', '/news/')

