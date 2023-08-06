from . import UniteGalleryCommon
from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.i18nmessageid import MessageFactory
from zope import schema
from collective.plonetruegallery.interfaces import IBaseSettings
_ = MessageFactory('collective.ptg.unitegallery')

class IUniteGalleryCompactSettings(IBaseSettings):
    """Unite Gallery Compact Settings"""

    #Theme options
    compact_theme_panel_position = schema.Choice(
        title=_(u"unitegallery_theme_panel_position_title", default=u"Thumbs panel position"),
        default=u'bottom',
        vocabulary=SimpleVocabulary([
            SimpleTerm('bottom', 'bottom', _(u"label_bottom", default=u"Bottom")),
            SimpleTerm('top', 'top', _(u"label_top", default=u"Top")),
            SimpleTerm('left', 'left', _(u"label_left", default=u"Left")),
            SimpleTerm('right', 'right', _(u"label_right", default=u"Right")),
        ]))
    compact_theme_hide_panel_under_width = schema.Int(
        title=_(u"unitegallery_theme_hide_panel_under_width_title", default=u"hide panel under certain browser width, if null, don't hide"),
        default=480)

    #Gallery options
    compact_gallery_width = schema.Int(
        title=_(u"unitegallery_gallery_width_title", default=u"Gallery width"),
        default=900)
    compact_gallery_height = schema.Int(
        title=_(u"unitegallery_gallery_height_title", default=u"Gallery height"),
        default=500)
    compact_gallery_min_width = schema.Int(
        title=_(u"unitegallery_gallery_min_width_title", default=u"Gallery minimal width when resizing"),
        default=400)
    compact_gallery_min_height = schema.Int(
        title=_(u"unitegallery_gallery_min_height_title", default=u"Gallery minimal height when resizing"),
        default=300)
    compact_gallery_skin = schema.Choice(
        title=_(u"unitegallery_gallery_skin_title", default=u"The global skin of the gallery"),
        description=_(u"unitegallery_gallery_skin_description", default=u"Will change all gallery items by default"),
        default=u'default',
        vocabulary=SimpleVocabulary([
            SimpleTerm('default', 'default', _(u"label_default", default=u"Default")),
            SimpleTerm('alexis', 'alexis', _(u"label_alexis", default=u"Alexis")),
        ]))
    compact_gallery_images_preload_type = schema.Choice(
        title=_(u"unitegallery_gallery_images_preload_type_title", default=u"Preload type of the images"),
        description=_(u"unitegallery_gallery_images_preload_type_description", default=u"Minimal - only image nabours will be loaded each time.\nVisible - visible thumbs images will be loaded each time.\nAll - load all the images first time."),
        default=u'minimal',
        vocabulary=SimpleVocabulary([
            SimpleTerm('minimal', 'minimal', _(u"label_minimal", default=u"Minimal")),
            SimpleTerm('visible', 'visible', _(u"label_visible", default=u"Visible")),
            SimpleTerm('all', 'all', _(u"label_all", default=u"All")),
        ]))
    compact_gallery_pause_on_mouseover = schema.Bool(
        title=_(u"unitegallery_gallery_pause_on_mouseover_title", default=u"Pause on mouseover when playing slideshow"),
        default=True)
    compact_gallery_control_thumbs_mousewheel = schema.Bool(
        title=_(u"unitegallery_gallery_control_thumbs_mousewheel_title", default=u"Enable / disable the mousewheel"),
        default=False)
    compact_gallery_control_keyboard = schema.Bool(
        title=_(u"unitegallery_gallery_control_keyboard_title", default=u"Enable / disble keyboard controls"),
        default=True)
    compact_gallery_carousel = schema.Bool(
        title=_(u"unitegallery_gallery_carousel_title", default=u"Next button on last image goes to first image"),
        default=True)
    compact_gallery_preserve_ratio = schema.Bool(
        title=_(u"unitegallery_gallery_preserve_ratio_title", default=u"Preserver ratio when on window resize"),
        default=True)
    compact_gallery_debug_errors = schema.Bool(
        title=_(u"unitegallery_gallery_debug_errors_title", default=u"Show error message when there is some error on the gallery area"),
        default=True)
    compact_gallery_background_color = schema.TextLine(
        title=_(u"unitegallery_gallery_background_color_title", default=u"Set custom background color. If not set it will be taken from css"),
        default=u'',
        required=False)


class UniteGalleryCompactType(UniteGalleryCommon):
    """Unite Gallery Compact"""
    name = u"unitegallery-compact"
    description = _('Unite Gallery Compact')
    theme = 'compact'
    schema = IUniteGalleryCompactSettings

UniteGalleryCompactSettings = createSettingsFactory(UniteGalleryCompactType.schema)
