from . import UniteGalleryCommon
from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.i18nmessageid import MessageFactory
from zope import schema
from collective.plonetruegallery.interfaces import IBaseSettings
_ = MessageFactory('collective.ptg.unitegallery')

class IUniteGalleryTilesgridSettings(IBaseSettings):
    """Unite Gallery Tilesgrid Settings"""

    #Main options
    tilesgrid_tile_width = schema.Int(
        title=_(u"unitegallery_tile_width_title", default=u"Tile width"),
        default=180)
    tilesgrid_tile_height = schema.Int(
        title=_(u"unitegallery_tile_height_title", default=u"Tile height"),
        default=150)
    tilesgrid_theme_gallery_padding = schema.Int(
        title=_(u"unitegallery_theme_gallery_padding_title", default=u"Padding from sides of the gallery"),
        default=0)
    tilesgrid_grid_padding = schema.Int(
        title=_(u"unitegallery_grid_padding_title", default=u"Set padding to the grid"),
        default=10)
    tilesgrid_grid_space_between_cols = schema.Int(
        title=_(u"unitegallery_grid_space_between_cols_title", default=u"Space between columns"),
        default=20)
    tilesgrid_grid_space_between_rows = schema.Int(
        title=_(u"unitegallery_grid_space_between_rows_title", default=u"Space between rows"),
        default=20)

    #Gallery options
    tilesgrid_gallery_width = schema.TextLine(
        title=_(u"unitegallery_gallery_width_title", default=u"Gallery width"),
        default=u"100%")
    tilesgrid_gallery_min_width = schema.Int(
        title=_(u"unitegallery_gallery_min_width_title", default=u"Gallery minimal width when resizing"),
        default=150)
    tilesgrid_gallery_background_color = schema.TextLine(
        title=_(u"unitegallery_gallery_background_color_title", default=u"Set custom background color. If not set it will be taken from css"),
        default=u'',
        required=False)


class UniteGalleryTilesgridType(UniteGalleryCommon):
    """Unite Gallery Default"""
    name = u"unitegallery-tilesgrid"
    description = _('Unite Gallery Tiles Grid')
    theme = 'tilesgrid'
    schema = IUniteGalleryTilesgridSettings

UniteGalleryTilesgridSettings = createSettingsFactory(UniteGalleryTilesgridType.schema)
