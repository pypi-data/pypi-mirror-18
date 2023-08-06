from __future__ import unicode_literals

import datetime

from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.db.models.signals import class_prepared
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


class Unit(models.Model):
    """
    A unit for a given attribute
    """
    name = models.CharField(_('name'), max_length=100, db_index=True)
    symbol = models.CharField(_('symbol'), max_length=10)

    def __unicode__(self):
        return self.name


class Attribute(models.Model):
    """
    An attribute for a model
    """
    TYPE_TEXT = 1
    TYPE_BOOLEAN = 2
    TYPE_INTEGER = 3
    TYPE_DECIMAL = 4
    TYPE_DATE = 5
    TYPE_TIME = 6
    TYPE_TAG = 7

    BOOLEAN_TRUE_TEXTS = ('TRUE', 'YES', 'T', 'Y', '1',)
    BOOLEAN_FALSE_TEXTS = ('FALSE', 'NO', 'F', 'N', '0',)
    BOOLEAN_NULL_TEXTS = ('NULL', '',)

    CHOICES_FOR_TYPE = (
        (TYPE_TEXT, _('text')),
        (TYPE_BOOLEAN, _('boolean')),
        (TYPE_INTEGER, _('integer')),
        (TYPE_DECIMAL, _('decimal')),
        (TYPE_DATE, _('date')),
        (TYPE_TIME, _('time')),
        (TYPE_TAG, _('tag')),
    )

    slug = models.SlugField(verbose_name=_('slug'), unique=True)
    name = models.CharField(_('name'), max_length=100, db_index=True)
    type = models.PositiveSmallIntegerField(_('type'), choices=CHOICES_FOR_TYPE)
    unit = models.ForeignKey('Unit', verbose_name=_('unit'), null=True, blank=True)

    def get_name_display(self):
        if self.name:
            return self.name
        return self.slug

    def get_label(self):
        label = self.get_name_display()
        if self.unit:
            label = '{label} ({symbol})'.format(
                    label=label,
                    symbol=self.unit.symbol,
            )
        return label

    def get_value_display(self, value):
        # If there are choices, try to get the choice representation
        if self.choice_set.exists():
            try:
                choice = Choice.objects.get(pk=value)
            except Choice.DoesNotExist:
                pass
            except MultipleObjectsReturned:
                pass
            else:
                return choice.get_value_display()
        # No choices or choices failed, just convert the value to string
        return '{}'.format(value)

    def get_choices(self):
        """
        Get choices for this attribute
        """

        # Standard choices for a boolean
        if self.type == self.TYPE_BOOLEAN:
            return (
                ('', _('unknown')),
                ('TRUE', _('yes')),
                ('FALSE', _('no')),
            )

        return [(choice.pk, choice.get_value_display()) for choice in self.choice_set.order_by('sort_order', 'name')]

    def text_to_int(self, text):
        """
        Convert text to integer
        """
        return int(text)

    def text_to_float(self, text):
        """
        Convert text to float
        """
        return float(text)

    def text_to_boolean(self, text):
        """
        Convert text to boolean
        """
        if text in self.BOOLEAN_TRUE_TEXTS:
            return True
        if text in self.BOOLEAN_FALSE_TEXTS:
            return False
        if text in self.BOOLEAN_NULL_TEXTS:
            return None
        raise ValueError(_('Value "{value}" is not a valid boolean.').format(value=text))

    def text_to_date(self, text):
        """
        Convert text to date
        """
        parts = text.split('-')
        return datetime.date(
                int(parts[0].strip()),
                int(parts[1].strip()),
                int(parts[2].strip()),
        )

    def text_to_time(self, text):
        """
        Convert text to time
        """
        parts = text.split(':')
        hours = int(parts[0].strip())
        try:
            minutes = int(parts[1].strip())
        except IndexError:
            minutes = 0
        try:
            seconds = int(parts[2].strip())
        except IndexError:
            seconds = 0
        return datetime.time(hours, minutes, seconds)

    def text_to_value(self, text):
        """
        Convert text to Python value
        """
        # Any text is valid text
        if self.type == self.TYPE_TEXT:
            return text
        # Copy, convert to uppercase and strip spaces
        t = text.upper().strip()
        # Try all other valid types
        if self.type == self.TYPE_INTEGER:
            return self.text_to_int(t)
        if self.type == self.TYPE_DECIMAL:
            return self.text_to_float(t)
        if self.type == self.TYPE_BOOLEAN:
            return self.text_to_boolean(t)
        if self.type == self.TYPE_DATE:
            return self.text_to_date(t)
        if self.type == self.TYPE_TIME:
            return self.text_to_time(t)
        # We cannot parse this type, use original variable ``text`` for error
        raise ValueError('Cannot convert text "{text}" to value of type {type}.'.format(
                text=text,
                type=self.get_type_display()
        ))

    def __unicode__(self):
        return self.get_name_display()

    def get_absolute_url(self):
        return reverse('attr_detail', kwargs={'pk': self.pk})


class Choice(models.Model):
    """
    A choice for the value of an attribute
    """
    attribute = models.ForeignKey(Attribute)
    value = models.CharField(_('value'), max_length=100, blank=True, db_index=True)
    name = models.CharField(_('name'), max_length=100, blank=True, db_index=True)
    description = models.TextField(_('description'), blank=True)
    sort_order = models.IntegerField(_('sort order'), default=0, db_index=True)

    def get_value_display(self):
        if self.name:
            return self.name
        return self.value

    def __unicode__(self):
        return '{attribute}.{name}'.format(attribute=self.attribute.name, name=self.get_value_display())

    class Meta:
        ordering = ['attribute_id', 'sort_order', 'value', 'pk', ]


class AbstractBaseAttr(models.Model):
    """
    An abstract Base Class used to generate actual Attr classes
    """
    attribute = models.ForeignKey(Attribute)
    value = JSONField(null=True, blank=True)

    class Meta:
        abstract = True


def createBaseAttr(model):
    class GeneratedAttr(AbstractBaseAttr):
        """
        An abstract Base Class used to generate actual Attr classes
        with an object
        """
        object = models.ForeignKey(model, related_name='attrs')

        _model = model

        class Meta:
            abstract = True
            unique_together = (('attribute', 'object'), )

    return GeneratedAttr


@receiver(class_prepared)
def attr_class_prepared(sender, **kwargs):
    if issubclass(sender, AbstractBaseAttr):
        if sender._model:
            sender._model._attrs_model = sender