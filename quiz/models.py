from django.db import models

# Create your models here.
class Quiz(models.Model):
	pass


class CategoryManager(models.Manager):
	def new_category(self, category):
		new_category = self.create(category=re.sub('\s+', '-', category).lower())

		new_category.save()
		return new_category


class Category(models.Model):

	category = models.CharField(
		verbose_name=('Category'),
		blank=False, null=False,
		unique=True, max_length=250)

	objects = CategoryManager()

	class Meta:
		verbose_name=('Category')
		verbose_name_plural=('Categories')


	def __str__(self):
		return self.category


class SubCategory(models.Model):
	sub_category = models.CharField(
		verbose_name=('Sub-Category'),
		blank=False, null=False,
		max_length=250)

	category = models.ForeignKey(Category,
		blank=False, null=False,
		verbose_name=('Category'),
		on_delete=models.CASCADE)

	objects = CategoryManager()

	class Meta:
		verbose_name=('Sub-Category')
		verbose_name_plural=('Sub-Categories')

	def __str__(self):
		return self.sub_category + "(" + self.category.category + ")"

# class DifficultyManager(models.Manager):
	

class Difficulty(models.Model):

	difficulty = models.CharField(
		verbose_name=('Difficulty'),
		blank=False, null=False,
		max_length=100
		)

	objects = DifficultyManager()



class Question(models.Model):
	"""
    Base class for all question types.
    Shared properties placed here.
    """

	quiz = models.ManyToManyField(Quiz, 
									verbose_name=('Quiz'),
									blank=True,)

	category = models.ForeignKey(Category,
								 blank=False,
								 null=False,
								 verbose_name=('Category'),
								 on_delete=models.CASCADE)

	sub_category = models.ForeignKey(Sub_category,
									 blank=False,
									 null=False,
									 verbose_name=('Sub-Category'),
									 on_delete=models.CASCADE)

	difficulty = models.ForeignKey(Difficulty,
									blank=False,
									null=False,
									verbose_name=('Difficulty'),
									on_delete=models.CASCADE)

	question_content = models.TextField(max_length=1000,
										blank=False,
										help_text=("Enter your question text"),
										verbose_name=('Question'))

	explanation = models.TextField(max_length=2000,
									blank=True,
									help_text=("Explanation to be shown"),
									verbose_name=('Explanation'))

	objects = InheritanceManager()

	class Meta:
		verbose_name = ('Question')
		verbose_name_plural = ('Questions')
		ordering = ['category']


	def __str__(self):
		return self.question_content