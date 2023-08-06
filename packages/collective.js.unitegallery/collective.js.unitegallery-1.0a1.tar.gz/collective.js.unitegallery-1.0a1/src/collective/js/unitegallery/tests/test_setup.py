# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.js.unitegallery.testing import COLLECTIVE_JS_UNITEGALLERY_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.js.unitegallery is properly installed."""

    layer = COLLECTIVE_JS_UNITEGALLERY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.js.unitegallery is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.js.unitegallery'))

    def test_browserlayer(self):
        """Test that ICollectiveJsUnitegalleryLayer is registered."""
        from collective.js.unitegallery.interfaces import (
            ICollectiveJsUnitegalleryLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectiveJsUnitegalleryLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_JS_UNITEGALLERY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.js.unitegallery'])

    def test_product_uninstalled(self):
        """Test if collective.js.unitegallery is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.js.unitegallery'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveJsUnitegalleryLayer is removed."""
        from collective.js.unitegallery.interfaces import ICollectiveJsUnitegalleryLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveJsUnitegalleryLayer, utils.registered_layers())
