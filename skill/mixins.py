from django.http import Http404

from dev.mixins import LoginRequiredMixin

from artisan.mixins import ArtisanAccountMixin

class SkillManagerMixin(ArtisanAccountMixin, object):
	def get_object(self, *args, **kwargs):
		artisan = self.get_account()
		obj = super(SkillManagerMixin, self).get_object(*args, **kwargs)
		try:
			obj.artisan  == artisan
		except:
			raise Http404

		if obj.artisan == artisan:
			return obj
		else:
			raise Http404
