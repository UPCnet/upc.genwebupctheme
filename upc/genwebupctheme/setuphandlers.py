def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('upc.genwebupctheme_various.txt') is None:
        import os,shutil
        buildout_folder = os.getcwd()
        shutil.copyfile('%s/src/upc.genwebupctheme/upc/genwebupctheme/skins/upc_genwebupctheme_custom_images/fck_strip.gif' % (buildout_folder),
                    '%s/eggs/Products.FCKeditor-2.6.3.1-py2.4.egg/Products/FCKeditor/skins/fckeditor/editor/skins/silver/fck_strip.gif' % (buildout_folder))
