from django.contrib import admin

from .models import Question, Category, SubCategory, Difficulty, Quiz
# Register your models here.

admin.site.register(Question)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Difficulty)
admin.site.register(Quiz)