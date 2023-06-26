from django  import forms
from .models import post,Profile



choice_list = [('Mental health','Mental health'),('heart disease','heart disease'),('covid 19','covid 19'),('immunization','immunization')]



class add_post_form(forms.ModelForm):
   
    class Meta:
        model = post
        fields=['title','summary','content','category','post_image','draft']

    Widgets = {
        'title':forms.TextInput(attrs={'class': 'form-control'}),
        'summary':forms.Textarea(attrs={'class': 'form-control',"Placeholder":choice_list}),
        'content':forms.Textarea(attrs={'class': 'form-control',"Placeholder":choice_list}),
        'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),

    }


class ProfilePage_Form(forms.ModelForm):
	class Meta:
		model = Profile
		exclude = ('user',)