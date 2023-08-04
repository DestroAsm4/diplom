import django_filters
from django.db import models
from django_filters import rest_framework

from goals.models import Goal, GoalCategory


class GoalDateFilter(rest_framework.FilterSet):
    class Meta:
        model = Goal
        fields = {
            'due_date': ('lte', 'gte'),
            'category': ('exact', 'in'),
            'status': ('exact', 'in'),
            'priority': ('exact', 'in'),
        }


class GoalCategoryFilter(rest_framework.FilterSet):
    class Meta:
        model = GoalCategory
        fields = ['board']
