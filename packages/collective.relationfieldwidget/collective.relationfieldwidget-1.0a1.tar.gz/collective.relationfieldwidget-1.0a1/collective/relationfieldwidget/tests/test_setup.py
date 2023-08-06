# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.relationfieldwidget.testing import COLLECTIVE_RELATIONFIELDWIDGET_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.relationfieldwidget is properly installed."""

    layer = COLLECTIVE_RELATIONFIELDWIDGET_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.relationfieldwidget is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('collective.relationfieldwidget'))

    def test_browserlayer(self):
        """Test that ICollectiveRelationfieldwidgetLayer is registered."""
        from collective.relationfieldwidget.interfaces import ICollectiveRelationfieldwidgetLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectiveRelationfieldwidgetLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_RELATIONFIELDWIDGET_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.relationfieldwidget'])

    def test_product_uninstalled(self):
        """Test if collective.relationfieldwidget is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled('collective.relationfieldwidget'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveRelationfieldwidgetLayer is removed."""
        from collective.relationfieldwidget.interfaces import ICollectiveRelationfieldwidgetLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveRelationfieldwidgetLayer, utils.registered_layers())
