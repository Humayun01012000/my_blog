from django import forms
from .models import Post, Category, Comment

# 📝 Form for Creating & Editing Posts
class PostForm(forms.ModelForm):
    new_category = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Or add new category...'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your post...'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        new_category_name = self.cleaned_data.get('new_category')

        if new_category_name:  # If user added a new category
            category, created = Category.objects.get_or_create(name=new_category_name)
            instance.category = category

        if commit:
            instance.save()
        return instance

# 🏷️ Form for Adding Categories
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
        }

# 💬 Form for Adding Comments (Supports Replies)
class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)  # Hidden field for replies

    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'Comment',
        }
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Write your comment...'}),
        }
