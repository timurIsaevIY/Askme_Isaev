from django import forms

from app.answers import Answer
from app.models import User
from app.questions import Question


class LoginForm(forms.Form):
    username = forms.CharField(max_length=10, min_length=4, required=True)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, required=True)

    def clean(self):
        super().clean()
        if 'username' not in self.cleaned_data:
            raise forms.ValidationError("empty username")
        if 'password' not in self.cleaned_data:
            raise forms.ValidationError("empty password")
        if self.cleaned_data['password'] == self.cleaned_data['username']:
            raise forms.ValidationError("password and username are the same")
        return self.cleaned_data


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']



    def clean(self):
        super().clean()
        if 'password' not in self.cleaned_data:
            raise forms.ValidationError("empty password")
        if 'confirm_password' not in self.cleaned_data:
            raise forms.ValidationError("empty confirm_password")
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise forms.ValidationError("passwords don't match")
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


class AddQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def clean(self):
        super().clean()
        if 'title' not in self.cleaned_data:
            raise forms.ValidationError("empty title")
        if 'text' not in self.cleaned_data:
            raise forms.ValidationError("empty text")
        # if 'tags' not in self.cleaned_data:
        #     raise forms.ValidationError("empty tags")
        return self.cleaned_data


class AddAnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'user', 'question']

    def clean(self):
        if 'text' not in self.cleaned_data:
            raise forms.ValidationError("empty text")