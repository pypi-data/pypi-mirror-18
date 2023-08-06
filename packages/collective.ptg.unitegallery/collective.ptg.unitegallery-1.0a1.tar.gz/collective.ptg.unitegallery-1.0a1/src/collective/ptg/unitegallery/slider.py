from . import UniteGalleryCommon
from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.i18nmessageid import MessageFactory
from zope import schema
from collective.plonetruegallery.interfaces import IBaseSettings
_ = MessageFactory('collective.ptg.unitegallery')

class IUniteGallerySliderSettings(IBaseSettings):
    """Unite Gallery Slider Settings"""


class UniteGallerySliderType(UniteGalleryCommon):
    """Unite Gallery Default"""
    name = u"unitegallery-slider"
    description = _('Unite Gallery Slider')
    theme = 'slider'
    schema = IUniteGallerySliderSettings

UniteGallerySliderSettings = createSettingsFactory(UniteGallerySliderType.schema)

