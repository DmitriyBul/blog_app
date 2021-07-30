from django import forms
from .models import Post


class PostCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('author')
        super(PostCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = ('title', 'text')
        exclude = ('author',)