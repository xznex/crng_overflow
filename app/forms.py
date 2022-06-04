from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'}),
                               max_length=30)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}), max_length=30)


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин..'}), max_length=30)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш email..'}), max_length=50)
    # nickname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль..'}), max_length=30)
    password_repeat = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль..'}), max_length=30)
    upload_avatar = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        if 'password' in cleaned_data and cleaned_data['password'] != cleaned_data['password_repeat']:
            self.add_error(None, "Passwords do not match")
        return cleaned_data


class SettingsForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Изменить логин'}), required=False,
        max_length=30)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Изменить email'}), required=False,
        max_length=50)
    new_avatar = forms.ImageField(required=False)

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        return user


class AskForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Дайте заголовок вопросу', 'style': 'font-size: large'}),
        max_length=150)
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'font-size: large', 'rows': 6,
                                     'placeholder': 'Расскажите подробней о вопросе...'}), max_length=2000)
    tags = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Укажите теги через запятую', 'style': 'font-size: large'}),
        max_length=75)


class AnswerForm(forms.Form):
    answer = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'font-size: large', 'rows': 4,
                                     'placeholder': 'Поделитесь своим ответом'}), max_length=2000)
