# -*- coding: utf-8 -*-
import logging
from Acquisition import ImplicitAcquisitionWrapper
from Products.CMFCore.utils import getToolByName
from z3c.form.interfaces import IFieldWidget
from z3c.form.widget import FieldWidget
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.interface import implementsOnly
from plone.app.z3cform.interfaces import IRelatedItemsWidget
from plone.app.z3cform.widget import RelatedItemsWidget
LOG = logging.getLogger(__name__)

class RelationWidget(RelatedItemsWidget):
    """RelatedItems widget for z3c.form with clickable list of URLs as output"""

    implementsOnly(IRelatedItemsWidget)

    def related_items(self):
        res = ()
        # Dexterity
        try:
            catalog = getToolByName(self.context, 'portal_catalog')
        except AttributeError:
            catalog = getToolByName(getSite(), 'portal_catalog')
        separator = self.separator
        if not self.value:
            return ()
        related = self.value.split(separator)
        if not related:
            return ()
        res = catalog(UID=related)
        return res


@implementer(IFieldWidget)
def RelationFieldWidget(field, request, extra=None):
    if extra is not None:
        request = extra
    return FieldWidget(field, RelationWidget(request))


