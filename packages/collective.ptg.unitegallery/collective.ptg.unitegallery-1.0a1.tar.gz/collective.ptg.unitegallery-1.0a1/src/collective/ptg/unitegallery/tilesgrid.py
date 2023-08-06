from . import UniteGalleryCommon
from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.i18nmessageid import MessageFactory
from zope import schema
from collective.plonetruegallery.interfaces import IBaseSettings
_ = MessageFactory('collective.ptg.unitegallery')

class IUniteGalleryTilesgridSettings(IBaseSettings):
    """Unite Gallery Tilesgrid Settings"""


class UniteGalleryTilesgridType(UniteGalleryCommon):
    """Unite Gallery Default"""
    name = u"unitegallery-tilesgrid"
    description = _('Unite Gallery Tiles Grid')
    theme = 'tilesgrid'
    schema = IUniteGalleryTilesgridSettings

UniteGalleryTilesgridSettings = createSettingsFactory(UniteGalleryTilesgridType.schema)
