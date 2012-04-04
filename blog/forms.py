from django import forms

from models import PostComment


class PostCommentForm(forms.ModelForm):
    author = forms.CharField(required=False)

    class Meta:
        model = PostComment
        exclude = ("post",)

    def clean_author(self):
        author = self.cleaned_data.get('author')
        return author if author else "Anonymous"

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 2:
            raise forms.ValidationError('At list 2 symbols!')
        else:
            return content

    def save(self, *args, **kwargs):
        post = kwargs.pop('post')
        comment = post.comments.create(
            author=self.cleaned_data['author'],
            content=self.cleaned_data['content']
        )
        return comment
