# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from booley.exceptions import BooleySyntaxError
from booley.parsers import Booley


def validate_booley_expression(expression, variables=None):
    try:
        parser = Booley()
        parser_result = parser.check_syntax(expression)
        if type(variables) == list:
            variables_not_found = list(set(parser.variables) - set(variables))
            if len(variables_not_found) > 0:
                raise ValidationError(_("Invalid variables: {0}".format(', '.join(variables_not_found))))
        return parser_result
    except BooleySyntaxError as e:
        raise ValidationError(str(e))
