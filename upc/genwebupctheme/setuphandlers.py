def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.
    if context.readDataFile('upc.genwebupctheme_various.txt') is None:
        pass
    import os,shutil

    #busquem l'ultima versio del fckeditor
    buildout_folder = os.getcwd()
    fckeditor_eggs = [dir for dir in os.listdir('%s/eggs/' % buildout_folder) if dir.upper().find('FCKEDITOR')>0]
    fckeditor_eggs.sort()
    fckeditor_path = fckeditor_eggs[-1]
    
    #busquem on tenim el tema
    genwebtheme_source = os.path.exists('%s/src/upc.genwebupctheme/' % buildout_folder) and 'src' or 'eggs'
    
    #sobreescrivim l'fckstrip
    shutil.copyfile('%s/%s/upc.genwebupctheme/upc/genwebupctheme/skins/upc_genwebupctheme_custom_images/fck_strip.gif' % (buildout_folder,genwebtheme_source),
                '%s/eggs/%s/Products/FCKeditor/skins/fckeditor/editor/skins/silver/fck_strip.gif' % (buildout_folder,fckeditor_path)) 
