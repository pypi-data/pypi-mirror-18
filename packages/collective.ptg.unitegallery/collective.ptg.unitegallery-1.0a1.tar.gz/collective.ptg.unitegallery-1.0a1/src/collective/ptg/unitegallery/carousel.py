from . import UniteGalleryCommon
from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.i18nmessageid import MessageFactory
from zope import schema
from collective.plonetruegallery.interfaces import IBaseSettings
_ = MessageFactory('collective.ptg.unitegallery')

class IUniteGalleryCarouselSettings(IBaseSettings):
    """Unite Gallery Carousel Settings"""


class UniteGalleryCarouselType(UniteGalleryCommon):
    """Unite Gallery Default"""
    name = u"unitegallery-carousel"
    description = _('Unite Gallery Carousel')
    theme = 'carousel'
    schema = IUniteGalleryCarouselSettings

UniteGalleryCarouselSettings = createSettingsFactory(UniteGalleryCarouselType.schema)
