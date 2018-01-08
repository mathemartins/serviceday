from django import forms

from django.utils.text import slugify

from skill.models import Skill

PUBLISH_CHOICES = (
	#('', ""),
	('publish', "Publish"),
	('draft', "Draft"),
)

class SkillAddForm(forms.Form):
	title = forms.CharField(label='Your Title', widget= forms.TextInput(
		attrs={
			"class": "custom-class",
			"placeholder": "Title",
		}))
	description = forms.CharField(widget=forms.Textarea(
			attrs={
				"class": "my-custom-class",
				"placeholder": "Description",
				"some-attr": "this",
			}
	)) #this might be a problem
	price  = forms.DecimalField()
	publish = forms.ChoiceField(widget=forms.RadioSelect, choices=PUBLISH_CHOICES, required=False)


	def clean_price(self):
		price = self.cleaned_data.get("price")
		if price <= 1000.00:
			raise forms.ValidationError("Price must be greater than #1000.00")
		elif price >= 100000.00:
			raise forms.ValidationError("Price must be less than #100000.00")
		else:
			return price

	def clean_title(self):
		title = self.cleaned_data.get("title")
		if len(title) > 3:
			return title
		else:
			raise forms.ValidationError("Title must be greater than 3 characters long.")



class SkillModelForm(forms.ModelForm):
	tags = forms.CharField(label='Related tags', required=False)
	publish = forms.ChoiceField(widget=forms.RadioSelect, choices=PUBLISH_CHOICES, required=False)
	# description = forms.CharField(widget=forms.Textarea(
	# 		attrs={
	# 			"class": "my-custom-class",
	# 			"placeholder": "Description",
	# 			"some-attr": "this",
	# 		}
	# ))
	class Meta:
		model = Skill
		fields = [
			"title",
			"description",
			"price",
			"image",
		]
		widgets = {
			"description": forms.Textarea(
					attrs={
						"placeholder": "New Description",
						"class": "form-control",
					}
				),
			"title": forms.TextInput(
				attrs= {
					"placeholder": "Title",
					"class": "form-control",
				}
			),
		}

	def clean(self, *args, **kwargs):
		cleaned_data = super(SkillModelForm, self).clean(*args, **kwargs)
		#title = cleaned_data.get("title")
		#slug = slugify(title)
		#qs = Product.objects.filter(slug=slug).exists()
		#if qs:
		# 	raise forms.ValidationError("Title is taken, new title is needed. Please try again.")
		return cleaned_data

	def clean_price(self):
		price = self.cleaned_data.get("price")
		if price <= 999.00:
			raise forms.ValidationError("Price must be greater than #999.00")
		elif price >= 100001.00:
			raise forms.ValidationError("Price must be less than #100,001.00")
		else:
			return price

	def clean_title(self):
		title = self.cleaned_data.get("title")
		if len(title) > 3:
			return title
		else:
			raise forms.ValidationError("Title must be greater than 3 characters long.")




















