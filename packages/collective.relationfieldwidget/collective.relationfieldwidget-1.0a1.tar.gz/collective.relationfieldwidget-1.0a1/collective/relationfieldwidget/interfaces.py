# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveRelationfieldwidgetLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""

from plone.app.z3cform.interfaces import IRelatedItemsWidget

class IRelationWidget(IRelatedItemsWidget):
   """Marker interface for RelationWidget"""
