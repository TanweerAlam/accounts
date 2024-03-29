from django.db import models

from django.utils.translation import ugettext_lazy as _
from quiz.models import Question


# Create your models here.

ANSWER_ORDER_OPTIONS = (
	('content', _('Content')),
	('random', _('Random')),
	('none', _('None'))
)


class MCQuestion(Question):

	answer_order = models.CharField(
		verbose_name=_('Answer Order'),
		help_text=_("The order in which multichoice "
                    "answer options are displayed "
                    "to the user"),
		max_length=30, null=True, blank=True,
		choices=ANSWER_ORDER_OPTIONS
		)

	def check_if_correct(self, guess):
		answer = Answer.objects.get(id=guess)

		if answer.correct is True:
			return True
		else:
			return False


	def order_answers(self, queryset):
		if self.answer_order == 'content':
			return self.queryset.order_by('content')
		if self.answer_order == 'random':
			return self.queryset.order_by('?')
		if self.answer_order == 'none':
			return self.queryset.order_by()

		return queryset


	def get_answers(self):
		return self.order_answers(Answer.objects.filter(question=self))

	def get_answers_list(self):
		return [(answer.id, answer.content) for answer in 
				self.queryset.order_by(Answer.objects.filter(question=self))]

	def answer_choice_to_string(self, guess):
		return Answer.objects.get(id=guess).content


	class Meta:
		verbose_name=_('Multiple Choice Question')
		verbose_name_plural=_('Multiple Choice Questions')