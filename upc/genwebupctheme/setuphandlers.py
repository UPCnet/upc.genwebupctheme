# -*- coding: utf-8 -*-
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
# from Products.Poi.Extensions.utils import addAction, removeAction

def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.
    if context.readDataFile('upc.genwebupctheme_various.txt') is None:
        pass
    
    properties = getToolByName(context, 'portal_properties')
    #import ipdb; ipdb.set_trace()
    properties.genwebupc_properties.titolespai_ca = 'à'.decode('utf-8')
    
    # import os,shutil
    # import upc.genwebupctheme
    # import Products.FCKeditor
    # 
    # fckeditor_path = os.path.dirname(Products.FCKeditor.__file__)
    # genwebtheme_path = os.path.dirname(upc.genwebupctheme.__file__)
    # 
    # #sobreescrivim l'fckstrip
    # shutil.copyfile('%s/skins/upc_genwebupctheme_custom_images/fck_strip.gif' % (genwebtheme_path),
    #             '%s/skins/fckeditor/editor/skins/silver/fck_strip.gif' % (fckeditor_path)) 
    # #sobreescrivim el fck_editor.css
    # shutil.copyfile('%s/skins/upc_genwebupctheme_styles/fck_editor.css' % (genwebtheme_path),
    #             '%s/skins/fckeditor/editor/skins/silver/fck_editor.css' % (fckeditor_path))
    # 
    # # Remove the log action inserted by POI
    # out = StringIO()
    # portal= context.getSite()
    # ttool = getToolByName(portal, 'portal_types')
    # removeAction(context, out, ttool, 'log', 'object')
    
