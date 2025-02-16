from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Category, Like, Comment
from .forms import PostForm, CategoryForm, CommentForm


# 📝 List all posts with pagination & search
def post_list(request):
    query = request.GET.get('q', '')
    posts = Post.objects.all().order_by('-created_at')

    if query:
        posts = posts.filter(title__icontains=query)  # 🔍 Search by title

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {'page_obj': page_obj, 'query': query})


# 📝 View a single post
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all().order_by('-created_at')
    form = CommentForm()

    liked = request.user.is_authenticated and post.likes.filter(user=request.user).exists()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'liked': liked,
    })


# ❤️ Like/Unlike a post (AJAX Support)
@csrf_exempt
@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        like.delete()  # Unlike if already liked

    return JsonResponse({'likes': post.likes.count(), 'liked': created})


# 🏷️ List posts by category
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
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, '✅ Post created successfully!')
            return redirect(post.get_absolute_url())
        else:
            messages.error(request, '⚠️ Please correct the form errors.')
    else:
        form = PostForm()

    return render(request, 'blog/add_post.html', {'form': form})


# ✍️ Edit a post (Only post owner)
@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.user != post.user:
        messages.error(request, "❌ You are not authorized to edit this post.")
        return redirect('post_list')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Post updated successfully!')
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})


# 🗑️ Delete a post (Only post owner, require POST request)
@login_required
@require_POST
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.user:
        messages.error(request, "❌ You are not authorized to delete this post.")
        return redirect('post_list')

    post.delete()
    messages.success(request, '✅ Post deleted successfully!')
    return redirect('post_list')


# 🏷️ Add a new category
@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Category added successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'blog/add_category.html', {'form': form})


# 📜 List all categories
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})


# 💬 Add a comment (AJAX Support)
@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            
            messages.success(request, "✅ Comment added successfully!")

            # Handle AJAX Request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'user': comment.user.username,
                    'content': comment.content,
                    'created_at': comment.created_at.strftime("%d %b %Y, %H:%M")
                })

            return redirect(post.get_absolute_url())

    return redirect(post.get_absolute_url())
