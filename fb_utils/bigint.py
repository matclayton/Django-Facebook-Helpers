"""module mydjangolib.bigint_patch

A fix for the rather well-known ticket #399 in the django project.

Create and link to auto-incrementing primary keys of type bigint without
having to reload the model instance after saving it to get the ID set in
the instance.
"""

from django.core import exceptions
from django.conf import settings
from django.db import connection
from django.db.models import fields
from django.utils.translation import ugettext as _

__version__ = "1.0"
__author__ = "Florian Leitner"

class BigIntegerField(fields.IntegerField):
    
    def db_type(self):
        if settings.DATABASE_ENGINE == 'mysql':
            return "bigint"
        elif settings.DATABASE_ENGINE == 'oracle':
            return "NUMBER(19)"
        elif settings.DATABASE_ENGINE[:8] == 'postgres':
            return "bigint"
        else:
            raise NotImplemented
    
    def get_internal_type(self):
        return "BigIntegerField"
    
    def to_python(self, value):
        if value is None:
            return value
        try:
            return long(value)
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                _("This value must be a long integer."))

class BigAutoField(fields.AutoField):
        
    def db_type(self):
        if settings.DATABASE_ENGINE == 'mysql':
            return "bigint AUTO_INCREMENT"
        elif settings.DATABASE_ENGINE == 'oracle':
            return "NUMBER(19)"
        elif settings.DATABASE_ENGINE[:8] == 'postgres':
            return "bigserial"
        else:
            raise NotImplemented
    
    def get_internal_type(self):
        return "BigAutoField"
    
    def to_python(self, value):
        if value is None:
            return value
        try:
            return long(value)
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                _("This value must be a long integer."))

class BigForeignKey(fields.related.ForeignKey):
    
    def db_type(self):
        rel_field = self.rel.get_related_field()
        # next lines are the "bad tooth" in the original code:
        if (isinstance(rel_field, BigAutoField) or
                (not connection.features.related_fields_match_type and
                isinstance(rel_field, BigIntegerField))):
            # because it continues here in the django code:
            # return IntegerField().db_type()
            # thereby fixing any AutoField as IntegerField
            return BigIntegerField().db_type()
        return rel_field.db_type()

################################
# SAMPLE IMPLEMENTATION (REMOVE) #
################################
#"""sample models.py implementation"""

#from django.db import models
#from mydjangolib import bigint_patch

#class VeryLargeModel(models.Model)
#    id = bigint_patch.BigAutoField(primary_key=True)
#    data = models.TextField()

#class ReferencingModel(models.Model)
#    id = bigint_patch.BigAutoField(primary_key=True)
#    target = bigint_patch.BigForeignKey(VeryLargeModel)
#    more_data = models.TextField()