from django import forms
from .models import Post, User, Category, Tags, Comment
class UserForm(forms.ModelForm):
    # first_name=forms.CharField(max_length=20)
    # last_name=forms.CharField(max_length=20)
    # email = forms.EmailField()
    address = forms.CharField(max_length=50)
    country = forms.CharField(max_length=20)
    # Birthday = forms.DateField( )
    city = forms.CharField(max_length=20)
    
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password',  'address', 'country', 'city', 'image', 'country')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'title', 'text', 'category', 'tags', 'post_image', 'featured_image')

class CommentForm(forms.ModelForm):
    # comment = forms.CharField(widget=forms.Textarea(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Leave a comment!',
    #     'rows': '4'
    # }))

    class Meta:
        model = Comment
        fields = ('name', 'email', 'massage')

# class ReplyForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('user', 'email', 'comment')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password', 'address', 'city', 'image')


# class UploadForm(forms.ModelForm):
#     excel_file = forms.FileField(upload_to='excel_uploads/')

#     class Meta: 
#         model = Hoteldata
#         fields = 'excel_file'