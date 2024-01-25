from django import forms
from core_app.models import *
class PackageReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "レヴューを書いてください"}))

    class Meta:
        model = PackageReview
        fields = ['review', 'rating']