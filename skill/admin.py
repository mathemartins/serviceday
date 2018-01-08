from django.contrib import admin

# Register your models here.
from skill.models import (
					Skill, 
					MySkills, 
					SkillRating,
					CuratedSkills
				)

class SkillAdmin(admin.ModelAdmin):
	list_display = ["__str__", "description", "price", "sale_price"]
	search_fields = ["title", "description"]
	list_filter = ["price", "sale_price"]
	list_editable = ["sale_price"]
	class Meta:
		model = Skill


admin.site.register(Skill, SkillAdmin)

admin.site.register(MySkills)
admin.site.register(SkillRating)
admin.site.register(CuratedSkills)