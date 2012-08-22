# Genweb 4.2: posat en la nevera, doncs es probable que al canviar el tipus de
# registre de configuracions de control panel no sigui necessari mes.

# from Products.GenericSetup.utils import PropertyManagerHelpers

# def _localinitProperties(self, node):
#     obj = self.context
#     if node.hasAttribute('i18n:domain'):
#         i18n_domain = str(node.getAttribute('i18n:domain'))
#         obj._updateProperty('i18n_domain', i18n_domain)
#     for child in node.childNodes:
#         if child.nodeName != 'property':
#             continue
#         prop_id = str(child.getAttribute('name'))
#         prop_map = obj.propdict().get(prop_id, None)

#         if prop_map is None:
#             if child.hasAttribute('type'):
#                 val = str(child.getAttribute('select_variable'))
#                 prop_type = str(child.getAttribute('type'))
#                 obj._setProperty(prop_id, val, prop_type)
#                 prop_map = obj.propdict().get(prop_id, None)
#             else:
#                 raise ValueError("undefined property '%s'" % prop_id)

#         if not 'w' in prop_map.get('mode', 'wd'):
#             raise BadRequest('%s cannot be changed' % prop_id)

#         elements = []
#         for sub in child.childNodes:
#             if sub.nodeName == 'element':
#                 value = sub.getAttribute('value')
#                 elements.append(value.encode(self._encoding))

#         if elements or prop_map.get('type') == 'multiple selection':
#             prop_value = tuple(elements) or ()
#         elif prop_map.get('type') == 'boolean':
#             prop_value = self._convertToBoolean(self._getNodeText(child))
#         else:
#             # if we pass a *string* to _updateProperty, all other values
#             # are converted to the right type
#             prop_value = self._getNodeText(child).encode(self._encoding)

#         if not self._convertToBoolean(child.getAttribute('purge')
#                                       or 'True'):
#             # If the purge attribute is False, merge sequences
#             prop = obj.getProperty(prop_id)
#             if isinstance(prop, (tuple, list)):
#                 prop_value = (tuple([p for p in prop
#                                      if p not in prop_value]) +
#                               tuple(prop_value))

#             else:
#                 if prop!="":
#                     prop_value = prop



#         obj._updateProperty(prop_id, prop_value)


# PropertyManagerHelpers._initProperties=_localinitProperties


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
