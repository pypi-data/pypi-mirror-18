# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.relationfieldwidget


class CollectiveRelationfieldwidgetLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.relationfieldwidget)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.relationfieldwidget:default')


COLLECTIVE_RELATIONFIELDWIDGET_FIXTURE = CollectiveRelationfieldwidgetLayer()


COLLECTIVE_RELATIONFIELDWIDGET_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_RELATIONFIELDWIDGET_FIXTURE,),
    name='CollectiveRelationfieldwidgetLayer:IntegrationTesting'
)


COLLECTIVE_RELATIONFIELDWIDGET_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_RELATIONFIELDWIDGET_FIXTURE,),
    name='CollectiveRelationfieldwidgetLayer:FunctionalTesting'
)


COLLECTIVE_RELATIONFIELDWIDGET_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_RELATIONFIELDWIDGET_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveRelationfieldwidgetLayer:AcceptanceTesting'
)
