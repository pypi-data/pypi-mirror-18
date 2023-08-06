# -*- coding: utf-8 -*-
"""Test Setup of ps.plone.fotorama."""

# python imports
try:
    import unittest2 as unittest
except ImportError:
    import unittest

# zope imports
from plone import api
from plone.browserlayer.utils import registered_layers

# local imports
from ps.plone.fotorama import (
    config,
    testing,
)


class TestSetup(unittest.TestCase):
    """Validate setup process for ps.plone.fotorama."""

    layer = testing.PS_PLONE_FOTORAMA_INTEGRATION_TESTING

    def setUp(self):
        """Additional test setup."""
        self.portal = self.layer['portal']
        plone_version = api.env.plone_version()
        self.has_plone4 = '3' < plone_version < '5'
        self.has_plone5 = '4' < plone_version < '6'

    def test_product_is_installed(self):
        """Validate that our product is installed."""
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled(config.PROJECT_NAME))

    def test_addon_layer(self):
        """Validate that the browserlayer for our product is installed."""
        layers = [l.getName() for l in registered_layers()]
        self.assertIn('IPloneFotoramaLayer', layers)

    def test_css_registered_plone4(self):
        """Validate that the CSS files are registered properly."""
        if not self.has_plone4:
            return
        css_registry = self.portal['portal_css']
        stylesheets_ids = css_registry.getResourceIds()
        self.assertIn(
            '++resource++ps.plone.fotorama/fotorama.css',
            stylesheets_ids,
        )

    def test_js_registered_plone4(self):
        """Validate that the JS files are registered properly."""
        if not self.has_plone4:
            return
        js_registry = self.portal['portal_javascripts']
        javascript_ids = js_registry.getResourceIds()
        self.assertIn(
            '++resource++ps.plone.fotorama/fotorama.js',
            javascript_ids,
        )


class UninstallTestCase(unittest.TestCase):

    layer = testing.PS_PLONE_FOTORAMA_INTEGRATION_TESTING

    def setUp(self):
        """Additional test setup."""
        self.portal = self.layer['portal']

        qi = self.portal.portal_quickinstaller
        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[config.PROJECT_NAME])

    def test_product_is_uninstalled(self):
        """Validate that our product is uninstalled."""
        qi = self.portal.portal_quickinstaller
        self.assertFalse(qi.isProductInstalled(config.PROJECT_NAME))

    def test_addon_layer_removed(self):
        """Validate that the browserlayer is removed."""
        layers = [l.getName() for l in registered_layers()]
        self.assertNotIn('IPloneFotoramaLayer', layers)
