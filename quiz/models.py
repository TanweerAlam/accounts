from django.db import models

from model_utils.managers import InheritanceManager

# Create your models here.
class Quiz(models.Model):

	title = models.CharField(
		verbose_name=('Title'),
		max_length=60, blank=False)

	description = models.TextField(
		verbose_name=('Description'),
		blank=True, help_text=('a description of the quiz'))

	url = models.SlugField(
		max_length=60, blank=False,
		verbose_name=('user friendly url'),
		help_text=('a user friendly url'))

	category = models.ForeignKey(
		Category, null=True, blank=True,
		verbose_name=('Category'), on_delete=models.CASCADE)

	random_order = models.BooleanField(
		default=False, blank=False,
		verbose_name=('Random Order'),
		help_text=_("Display the questions in "
                    "a random order or as they "
                    "are set?"))

	max_questions = models.PositiveIntegerField(
		default=10, blank=True,
		verbose_name=('Max Questions'),
		help_text=_("Number of questions to be answered on each attempt."))

	answers_at_end = models.BooleanField(
		default=True, blank=False,
		help_text=_("Correct answer is NOT shown after question."
                    " Answers displayed at the end."),
        verbose_name=_("Answers at end"))

	exam_paper = models.BooleanField(
		default=False, blank=False,
		help_text=_("If yes, the result of each"
                    " attempt by a user will be"
                    " stored. Necessary for marking."),
        verbose_name=_("Exam Paper"))

	single_attempt = models.BooleanField(
		blank=False, default=False,
		help_text=_("If yes, only one attempt by"
                    " a user will be permitted."
                    " Non users cannot sit this exam."),
        verbose_name=_("Single Attempt"))

	pass_mark = models.SmallIntegerField(
		blank=True, default=0,
		verbose_name=_("Pass Mark"),
        help_text=_("Percentage required to pass exam."),
        validators=[MaxValueValidator(100)])

	success_text = models.TextField(
		blank=True, help_text=_("Displayed if user passes."),
        verbose_name=_("Success Text"))

	fail_text = models.TextField(
		verbose_name=_("Fail Text"),
        blank=True, help_text=_("Displayed if user fails."))

	draft = models.BooleanField(
		blank=True, default=False,
        verbose_name=_("Draft"),
        help_text=_("If yes, the quiz is not displayed"
                    " in the quiz list and can only be"
                    " taken by users who can edit"
                    " quizzes."))

	def save(self, force_insert=False, force_update=False, *args, **kwargs):
		self.url = re.sub('\s+', '-', self.url).lower()

		self.url = ''.join(letter for letter in self.url if 
							letter.isalnum() or letter == '-')

		if self.single_attempt is True:
			self.exam_paper = True

		if self.pass_mark > 100:
			raise ValidationError('%s is above 100' % self.pass_mark)

		super(Quiz, self).save(force_insert, force_update, *args, **kwargs)

	class Meta:
		verbose_name=('Quiz')
		verbose_name_plural=('Quizzes')


	def __str__(self):
		return self.title


	def get_questions(self):
		return self.question_set.all().select_subclasses()

	@property
	def get_max_score(self):
		return self.get_questions().count()

	# Details of anonymous user

	def anon_score_id(self):
		return str(self.id)+'_score'

	def anon_q_list(self):
		return str(self.id)+'_q_list'

	def anon_q_data(self):
		return str(self.id)+'_q_data'
	

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

class DifficultyManager(models.Manager):
 	pass


class Difficulty(models.Model):

	difficulty = models.CharField(
		verbose_name=('Difficulty'),
		blank=False, null=False,
		max_length=100
		)

	objects = DifficultyManager()

	class Meta:
		verbose_name=('Difficulty')


	def __str__(self):
		return self.difficulty

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

	sub_category = models.ForeignKey(SubCategory,
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