from . import UniteGalleryCommon
from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.i18nmessageid import MessageFactory
from zope import schema
from collective.plonetruegallery.interfaces import IBaseSettings
_ = MessageFactory('collective.ptg.unitegallery')

class IUniteGalleryCarouselSettings(IBaseSettings):
    """Unite Gallery Carousel Settings"""

    #Main options
    carousel_tile_width = schema.Int(
        title=_(u"unitegallery_tile_width_title", default=u"Tile width"),
        default=180)
    carousel_tile_height = schema.Int(
        title=_(u"unitegallery_tile_height_title", default=u"Tile height"),
        default=150)
    carousel_theme_gallery_padding = schema.Int(
        title=_(u"unitegallery_theme_gallery_padding_title", default=u"Padding from sides of the gallery"),
        default=0)
    carousel_theme_carousel_align = schema.Choice(
        title=_(u"unitegallery_theme_carousel_align_title", default=u"The align of the carousel"),
        default='center',
        vocabulary=SimpleVocabulary([
            SimpleTerm('left', 'left', _(u"label_left", default=u"Left")),
            SimpleTerm('center', 'center', _(u"label_center", default=u"Center")),
            SimpleTerm('right', 'right', _(u"label_right", default=u"Right")),
        ]))
    carousel_theme_carousel_offset = schema.Int(
        title=_(u"unitegallery_theme_carousel_offset_title", default=u"The offset of the carousel from the align sides"),
        default=0)
					
    #Gallery options
    carousel_gallery_width = schema.TextLine(
        title=_(u"unitegallery_gallery_width_title", default=u"Gallery width"),
        default=u"100%")
    carousel_gallery_min_width = schema.Int(
        title=_(u"unitegallery_gallery_min_width_title", default=u"Gallery minimal width when resizing"),
        default=150)
    carousel_gallery_background_color = schema.TextLine(
        title=_(u"unitegallery_gallery_background_color_title", default=u"Set custom background color. If not set it will be taken from css"),
        default=u'',
        required=False)


class UniteGalleryCarouselType(UniteGalleryCommon):
    """Unite Gallery Default"""
    name = u"unitegallery-carousel"
    description = _('Unite Gallery Carousel')
    theme = 'carousel'
    schema = IUniteGalleryCarouselSettings

UniteGalleryCarouselSettings = createSettingsFactory(UniteGalleryCarouselType.schema)
