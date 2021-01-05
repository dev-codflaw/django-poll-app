from django.db import models

# Create your models here.


class Label(models.Model):
	# DEFAULT_PK = 1
	title = models.CharField(max_length=50)
	description = models.CharField(max_length=300, blank=True)
	color = models.CharField(max_length=10, blank=True)
	status = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'labels'
		verbose_name = 'label'
		verbose_name_plural = 'labels'


class Contacts(models.Model):
	first_name = models.CharField(max_length=30, blank=True)
	last_name = models.CharField(max_length=30, blank=True)
	email = models.CharField(max_length=50)
	contact_number = models.CharField(max_length=20, blank=True)
	labels = models.ManyToManyField(Label)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	def __str__(self):
		return self.first_name


	def get_fullname(self):
		return "%s %s" % (self.first_name, self.last_name)


	class Meta:
		db_table = 'contacts'
		verbose_name = 'Contact'
		verbose_name_plural = 'Contacts'


