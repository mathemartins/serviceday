from django import forms
from artisan.models import ArtisanAccount

class NewArtisanForm(forms.ModelForm):
	agree = forms.BooleanField(label='Agree to Terms', widget=forms.CheckboxInput(attrs={'class':'form-control'}))
	
	class Meta:
		model = ArtisanAccount
		fields = [
			"address",
			"mobile_number",
		]
		widgets = {
			"address": forms.TextInput(
					attrs={
						"placeholder": "Enter Address Of Physical Location",
						"class": "form-control",
					}
				),
			"mobile_number": forms.TextInput(
				attrs= {
					"placeholder": "format: 07012345678",
					"class": "form-control",
				}
			)
		}