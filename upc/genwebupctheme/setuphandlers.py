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
    
    # GW4, per solucionar el problema de unicode en les portal_properties
    properties = getToolByName(context, 'portal_properties')
    properties.genwebupc_properties.titolespai_ca = "Títol de l'espai en català".decode('utf-8')
    properties.genwebupc_properties.titolespai_es = "Títol de l'espai en castellà".decode('utf-8')
    properties.genwebupc_properties.titolespai_en = "Títol de l'espai en anglès".decode('utf-8')
    properties.genwebupc_properties.firmaunitat_ca = "Firma de la unitat en català".decode('utf-8')
    properties.genwebupc_properties.firmaunitat_es = "Firma de la unitat en castellà".decode('utf-8')
    properties.genwebupc_properties.firmaunitat_en = "Firma de la unitat en anglès".decode('utf-8')
    properties.genwebupc_properties.enllaslogotipdretalt = "Universitat Politècnica de Catalunya".decode('utf-8')
    properties.genwebupc_properties.ambitdoctorat_ca = "Àmbit doctorat - [català]".decode('utf-8')
    properties.genwebupc_properties.ambitdoctorat_es = "Àmbit doctorat - [castellà]".decode('utf-8')
    properties.genwebupc_properties.ambitdoctorat_en = "Àmbit doctorat - [anglès]".decode('utf-8')
                                    
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
    
