from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from user_app.models import *


class RegisterForm(UserCreationForm):
    PREFECTURE_CHOICES = [
        ('', '都道府県を選択してください'),
        ('Hokkaido', '北海道'),
        ('Aomori', '青森県'),
        ('Iwate', '岩手県'),
        ('Miyagi', '宮城県'),
        ('Akita', '秋田県'),
        ('Yamagata', '山形県'),
        ('Fukushima', '福島県'),
        ('Ibaraki', '茨城県'),
        ('Tochigi', '栃木県'),
        ('Gunma', '群馬県'),
        ('Saitama', '埼玉県'),
        ('Chiba', '千葉県'),
        ('Tokyo', '東京都'),
        ('Kanagawa', '神奈川県'),
        ('Niigata', '新潟県'),
        ('Toyama', '富山県'),
        ('Ishikawa', '石川県'),
        ('Fukui', '福井県'),
        ('Yamanashi', '山梨県'),
        ('Nagano', '長野県'),
        ('Gifu', '岐阜県'),
        ('Shizuoka', '静岡県'),
        ('Aichi', '愛知県'),
        ('Mie', '三重県'),
        ('Shiga', '滋賀県'),
        ('Kyoto', '京都府'),
        ('Osaka', '大阪府'),
        ('Hyogo', '兵庫県'),
        ('Nara', '奈良県'),
        ('Wakayama', '和歌山県'),
        ('Tottori', '鳥取県'),
        ('Shimane', '島根県'),
        ('Okayama', '岡山県'),
        ('Hiroshima', '広島県'),
        ('Yamaguchi', '山口県'),
        ('Tokushima', '徳島県'),
        ('Kagawa', '香川県'),
        ('Ehime', '愛媛県'),
        ('Kochi', '高知県'),
        ('Fukuoka', '福岡県'),
        ('Saga', '佐賀県'),
        ('Nagasaki', '長崎県'),
        ('Kumamoto', '熊本県'),
        ('Oita', '大分県'),
        ('Miyazaki', '宮崎県'),
        ('Kagoshima', '鹿児島県'),
        ('Okinawa', '沖縄県'),
    ]
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ユーザ名'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'メールアドレス'}))
    location = forms.ChoiceField(choices=PREFECTURE_CHOICES, widget=forms.Select(attrs={'placeholder': '都道府県を選択してください'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'パスワード'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '確認パスワード'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'location', 'password1', 'password2']
        verbose_name_plural = '新規登録'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise forms.ValidationError('メールアドレスがもう登録しました')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        username = self.cleaned_data.get('username')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('パスワードに誤りがあります')
            if username and password1 and username in password1:
                raise forms.ValidationError('パスワードがユーザ名と類似しています')
        return password2
