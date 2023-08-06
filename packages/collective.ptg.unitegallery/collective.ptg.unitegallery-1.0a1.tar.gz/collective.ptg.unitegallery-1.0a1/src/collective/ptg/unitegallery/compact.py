from . import UniteGalleryCommon
from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.i18nmessageid import MessageFactory
from zope import schema
from collective.plonetruegallery.interfaces import IBaseSettings
_ = MessageFactory('collective.ptg.unitegallery')

class IUniteGalleryCompactSettings(IBaseSettings):
    """Unite Gallery Compact Settings"""


class UniteGalleryCompactType(UniteGalleryCommon):
    """Unite Gallery Compact"""
    name = u"unitegallery-compact"
    description = _('Unite Gallery Compact')
    theme = 'compact'
    schema = IUniteGalleryCompactSettings

UniteGalleryCompactSettings = createSettingsFactory(UniteGalleryCompactType.schema)
