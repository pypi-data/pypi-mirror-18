# -*- coding: utf-8 -*-
from django.db import models

from django_booley.validators import validate_booley_expression


class BooleyField(models.TextField):

    def __init__(self, valid_variables=None, *args, **kwargs):
        self.valid_variables = valid_variables
        super(BooleyField, self).__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super(BooleyField, self).validate(value, model_instance)
        return validate_booley_expression(value, self.valid_variables)
