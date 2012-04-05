from django import forms
from django.forms.widgets import HiddenInput

from models import PostComment, SimpleSpamProtection


class PostCommentForm(forms.ModelForm):
    author = forms.CharField(required=False)
    question = forms.CharField(widget=HiddenInput)
    answer = forms.IntegerField()

    class Meta:
        model = PostComment
        exclude = ("post",)

    def __init__(self, *args, **kwargs):
        super(PostCommentForm, self).__init__(*args, **kwargs)
        if not 'question' in self.data:
            self.protection = SimpleSpamProtection.objects.all().order_by('?')[0]
            self.initial['question'] = self.protection.id
        else:
            self.protection = SimpleSpamProtection.objects.get(id=self.data['question'])
        self.fields['answer'].label = 'Answer the question: %s' % self.protection.question

    def clean_author(self):
        author = self.cleaned_data.get('author')
        return author if author else "Anonymous"

    def clean_answer(self):
        if not self.cleaned_data.get('answer') == self.protection.answer:
            raise forms.ValidationError('Give right answer, please!')

    def save(self, *args, **kwargs):
        post = kwargs.pop('post')
        comment = post.comments.create(
            author=self.cleaned_data['author'],
            content=self.cleaned_data['content']
        )
        return comment
