from . import UniteGalleryCommon
from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.i18nmessageid import MessageFactory
from zope import schema
from collective.plonetruegallery.interfaces import IBaseSettings
_ = MessageFactory('collective.ptg.unitegallery')

class IUniteGalleryGridSettings(IBaseSettings):
    """Unite Gallery Grid Settings"""


class UniteGalleryGridType(UniteGalleryCommon):
    """Unite Gallery Default"""
    name = u"unitegallery-grid"
    description = _('Unite Gallery Grid')
    theme = 'grid'
    schema = IUniteGalleryGridSettings

UniteGalleryGridSettings = createSettingsFactory(UniteGalleryGridType.schema)
