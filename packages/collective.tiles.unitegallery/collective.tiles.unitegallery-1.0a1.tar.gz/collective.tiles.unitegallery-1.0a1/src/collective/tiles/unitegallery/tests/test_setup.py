# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.tiles.unitegallery.testing import COLLECTIVE_TILES_UNITEGALLERY_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.tiles.unitegallery is properly installed."""

    layer = COLLECTIVE_TILES_UNITEGALLERY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.tiles.unitegallery is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.tiles.unitegallery'))

    def test_browserlayer(self):
        """Test that ICollectiveTilesUnitegalleryLayer is registered."""
        from collective.tiles.unitegallery.interfaces import (
            ICollectiveTilesUnitegalleryLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectiveTilesUnitegalleryLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_TILES_UNITEGALLERY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.tiles.unitegallery'])

    def test_product_uninstalled(self):
        """Test if collective.tiles.unitegallery is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.tiles.unitegallery'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveTilesUnitegalleryLayer is removed."""
        from collective.tiles.unitegallery.interfaces import ICollectiveTilesUnitegalleryLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveTilesUnitegalleryLayer, utils.registered_layers())
