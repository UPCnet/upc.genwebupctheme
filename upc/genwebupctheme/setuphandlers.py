def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('upc.genwebupctheme_various.txt') is None:
        return
    
    site = context.getSite()
    if not getattr(site,'logos_peu',False):
        site.invokeFactory(id='logos_peu',title='logos_peu',type_name='Logos Container')        
