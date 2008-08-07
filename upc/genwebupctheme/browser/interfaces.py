from plone.theme.interfaces import IDefaultPloneLayer

class IThemeSpecificNeutre(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
       If you need to register a viewlet only for the
       "Tema genwebUPC" theme, this interface must be its layer
       (in genwebupctheme/viewlets/configure.zcml).
    """
