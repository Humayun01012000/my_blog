from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from .models import Post, Category
from .forms import PostForm, CategoryForm

# 📝 List all posts with pagination
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})

# 📝 View a single post
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})

# 🏷️ List posts by category with pagination
def category_posts(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(category=category).order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/category_posts.html', {'page_obj': page_obj, 'category': category})

# ✍️ Add a new post (Only logged-in users)
@login_required
def add_post(request):
    categories = Category.objects.all()  # Fetch existing categories

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Assign the logged-in user

            # Handle new category addition
            category_input = request.POST.get('category')
            if category_input and category_input.startswith('new:'):
                category_name = category_input.replace('new:', '').strip()
                category, created = Category.objects.get_or_create(name=category_name)
                post.category = category
            else:
                post.category = form.cleaned_data['category']

            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect(post.get_absolute_url())

    else:
        form = PostForm()

    return render(request, 'blog/add_post.html', {'form': form, 'categories': categories})

# ✏️ Edit an existing post (Only post owner)
@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Prevent unauthorized access
    if request.user != post.user:
        messages.error(request, "You are not authorized to edit this post.")
        return redirect('post_list')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

# 🗑️ Delete a post (Only post owner, require POST request)
@login_required
@require_POST  # Ensure only POST requests can delete a post
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.user != post.user:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('post_list')

    post.delete()
    messages.success(request, 'Post deleted successfully!')
    return redirect('post_list')

# 🏷️ Add a new category
@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'blog/add_category.html', {'form': form})

# 📜 List all categories
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})
