from Products.CMFPlone.utils import getFSVersionTuple
from Products.CMFCore.utils import getToolByName


def upgradeSolgemaFlowView108(context):
    portal_setup = getToolByName(context, 'portal_setup')
    if getFSVersionTuple()[0] == 4:
        portal_setup.runAllImportStepsFromProfile('profile-Solgema.FlowView.upgrades:solgemaflowview_upgrade108_plone4')
    else:
        portal_setup.runAllImportStepsFromProfile('profile-Solgema.FlowView.upgrades:solgemaflowview_upgrade108_plone5')
