from Products.CMFCore.utils import getToolByName


def v1001(context):
    portal_css = getToolByName(context, 'portal_css')
    portal_css.unregisterResource('++resource++collective.js.fancytree/ui.fancytree.css')
    context.runAllImportStepsFromProfile('profile-collective.js.fancytree:default')
    context.runAllImportStepsFromProfile('profile-collective.js.fancytree:theme-lion')
