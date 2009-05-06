## Script (Python) "pre_go_back"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Registered
##

from Products.CMFCore.utils import getToolByName

portal = getToolByName(context, 'portal_url').getPortalObject()
state.setContext(portal)

return state