from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Book
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BookCreateForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http.response import JsonResponse

class HomeView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'home.html'
    ordering = '-created_at'
    login_url = 'index'
    redirect_field_name = 'redirect_to'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BookCreateForm
        return context

    def post(self, request, *args, **kwargs):
        form = BookCreateForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            new_book = form.save(commit=False)
            new_book.uploaded_by = self.request.user
            new_book.save()
            new_book.users_who_like.add(self.request.user)
            messages.success(self.request, 'successfully added!!')
            return redirect('home')
        else:
            all_book = Book.objects.all().order_by('-created_at')
            paginator = Paginator(all_book, 3)
            page_number = request.GET.get('page')
            object_list = paginator.get_page(page_number)
            context = {
                'form': form,
                'object_list': object_list,
                'page_obj': object_list,
            }
            return render(self.request, 'home.html', context=context)

class BookDetailView(DetailView):
    model = Book
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = BookCreateForm()
        form.fields['title'].initial = self.object.title
        form.fields['description'].initial = self.object.description
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, id=self.kwargs['pk'])
        form = BookCreateForm(self.request.POST, self.request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('detail', self.kwargs['pk'])
        else:
            context = {
                'form': form,
                'object': get_object_or_404(Book, id=self.kwargs['pk']),
            }
            return render(self.request, 'detail.html', context=context)

def delete_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    book.delete()
    return redirect('home')

def add_favorite(request, pk, page):
    book = get_object_or_404(Book, id=pk)
    book.users_who_like.add(request.user)
    book.save()
    if page == 'detail':
        return redirect('detail', pk=pk)
    else:
        context = {
            'user': request.user,
            'book': book,
        }
        html = render_to_string('partial/favorite.html', context)
        return JsonResponse({'html': html})

def remove_favorite(request, pk, page):
    book = get_object_or_404(Book, id=pk)
    book.users_who_like.remove(request.user)
    book.save()
    if page == 'detail':
        return redirect('detail', pk=pk)
    else:
        context = {
            'user': request.user,
            'book': book,
        }
        html = render_to_string('partial/favorite.html', context)
        return JsonResponse({'html': html})
