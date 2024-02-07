from django import forms
from core_app.models import *
class PackageReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "レヴューを書いてください"}))

    class Meta:
        model = PackageReview
        fields = ['review', 'rating']


class Stepone(forms.Form):
    inoutactivity_choices = [(activity.id, activity.title) for activity in OutInActivity.objects.all()]
    INOUT_CHOICES = inoutactivity_choices
    
    activities = forms.MultipleChoiceField(required=False,widget=forms.CheckboxSelectMultiple, choices=INOUT_CHOICES, label="あなたはどのようにして過ごしていますか❓" )

class Steptwo(forms.Form):
    personality_choices = [(personality.id, personality.title) for personality in Personality.objects.all()]
    PERSONALITY_CHOICES = personality_choices
    
    personalities = forms.MultipleChoiceField(required=False,widget=forms.CheckboxSelectMultiple, choices=PERSONALITY_CHOICES, label="どのようにして過ごすのが好きですか❓" )

    
class Stepthree(forms.Form):
    subcategory_choices = [(subcategory.id, subcategory.title) for subcategory in SubCategory.objects.all()]
    SUBCATEGORY_CHOICES = subcategory_choices
    
    subcategories = forms.MultipleChoiceField(required=False,widget=forms.CheckboxSelectMultiple, choices=SUBCATEGORY_CHOICES, label="場所の中にあるもの❓" )

class Stepfour(forms.Form):
    transport_choices = [(transport.id, transport.title) for transport in Transport.objects.all()]
    Transport_CHOICES = transport_choices
    
    transports = forms.MultipleChoiceField(required=False,widget=forms.CheckboxSelectMultiple, choices=Transport_CHOICES, label="公共交通機関アクセス❓" )

class Stepfive(forms.Form):
    parking_choices = [(parking.id, parking.title) for parking in Parking.objects.all()]
    PARKING_CHOICES = parking_choices
    
    parkings = forms.MultipleChoiceField(required=False,widget=forms.CheckboxSelectMultiple, choices=PARKING_CHOICES, label="駐車場❓" )

class Stepsix(forms.Form):
    address_choices = [(address.id, address.title) for address in Location.objects.all()]
    Address_CHOICES = address_choices
    
    addresses = forms.MultipleChoiceField(required=False,widget=forms.CheckboxSelectMultiple, choices=Address_CHOICES, label="どこの県に行きたいですか❓" )