# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from Products.CMFPlone.utils import getFSVersionTuple


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'collective.js.unitegallery:uninstall',
            'collective.js.unitegallery:plone4',
            'collective.js.unitegallery:plone5',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    site = context.getSite()

    if getFSVersionTuple()[0] == 4:
        setup.runAllImportStepsFromProfile('profile-collective.js.unitegallery:plone4')
        jstool = getToolByName(site, 'portal_javascripts')
        jstool.cookResources()
        csstool = getToolByName(site, 'portal_css')
        csstool.cookResources()
    else:
        setup.runAllImportStepsFromProfile('profile-collective.js.unitegallery:plone5')

def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
