from . import UniteGalleryCommon
from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.i18nmessageid import MessageFactory
from zope import schema
from collective.plonetruegallery.interfaces import IBaseSettings
_ = MessageFactory('collective.ptg.unitegallery')

class IUniteGalleryVideoSettings(IBaseSettings):
    """Unite Gallery Video Settings"""

class UniteGalleryVideoType(UniteGalleryCommon):
    """Unite Gallery Default"""
    name = u"unitegallery-video"
    description = _('Unite Gallery Video')
    theme = 'video'
    schema = IUniteGalleryVideoSettings

UniteGalleryVideoSettings = createSettingsFactory(UniteGalleryVideoType.schema)
