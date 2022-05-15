from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class SignupForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # nickname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    upload_avatar = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        if 'password' in cleaned_data and cleaned_data['password'] != cleaned_data['password_repeat']:
            self.add_error(None, "Passwords do not match")
        return cleaned_data


class SettingsForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    new_avatar = forms.ImageField(required=False)


class AskForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Указывайте через запятую'}))


class AnswerForm(forms.Form):
    answer = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'font-size: large', 'rows': 3,
                                     'placeholder': 'Enter your answer here...'}))
