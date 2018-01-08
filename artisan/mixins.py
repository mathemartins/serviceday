import datetime
from django.db.models import Count, Min, Sum, Avg, Max
from artisan.models import ArtisanAccount

# from billing.models import Transaction
from dev.mixins import LoginRequiredMixin
from skill.models import Skill



class ArtisanAccountMixin(LoginRequiredMixin, object):
	account = None
	skills = []
	transactions = []

	def get_account(self):
		user = self.request.user
		accounts = ArtisanAccount.objects.filter(user=user)
		if accounts.exists() and accounts.count() == 1:
			self.account = accounts.first()
			return accounts.first()
		return None

	def get_skills(self):
		account = self.get_account()
		skills = Skill.objects.filter(artisan=account)
		self.skills = skills
		return skills

	# def get_transactions(self):
	# 	products = self.get_products()
	# 	transactions = Transaction.objects.filter(product__in=products)
	# 	return transactions

	# def get_transactions_today(self):
	# 	today = datetime.date.today()
	# 	today_min = datetime.datetime.combine(today, datetime.time.min)
	# 	today_max = datetime.datetime.combine(today, datetime.time.max)
	# 	return self.get_transactions().filter(timestamp__range=(today_min, today_max))

	# def get_total_sales(self):
	# 	transactions = self.get_transactions().aggregate(Sum("price"), Avg("price"))
	# 	print transactions
	# 	total_sales = transactions["price__sum"]
	# 	return total_sales

	# def get_today_sales(self):
	# 	transactions = self.get_transactions_today().aggregate(Sum("price"))
	# 	total_sales = transactions["price__sum"]
	# 	return total_sales