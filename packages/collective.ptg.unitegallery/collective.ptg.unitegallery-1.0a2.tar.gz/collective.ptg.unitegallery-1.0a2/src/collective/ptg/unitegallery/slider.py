from . import UniteGalleryCommon
from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.i18nmessageid import MessageFactory
from zope import schema
from collective.plonetruegallery.interfaces import IBaseSettings
_ = MessageFactory('collective.ptg.unitegallery')

class IUniteGallerySliderSettings(IBaseSettings):
    """Unite Gallery Slider Settings"""


    #Gallery options
    slider_gallery_width = schema.Int(
        title=_(u"unitegallery_gallery_width_title", default=u"Gallery width"),
        default=900)
    slider_gallery_height = schema.Int(
        title=_(u"unitegallery_gallery_height_title", default=u"Gallery height"),
        default=500)
    slider_gallery_min_width = schema.Int(
        title=_(u"unitegallery_gallery_min_width_title", default=u"Gallery minimal width when resizing"),
        default=400)
    slider_gallery_min_height = schema.Int(
        title=_(u"unitegallery_gallery_min_height_title", default=u"Gallery minimal height when resizing"),
        default=300)
    slider_gallery_skin = schema.Choice(
        title=_(u"unitegallery_gallery_skin_title", default=u"The global skin of the gallery"),
        description=_(u"unitegallery_gallery_skin_description", default=u"Will change all gallery items by default"),
        default=u'default',
        vocabulary=SimpleVocabulary([
            SimpleTerm('default', 'default', _(u"label_default", default=u"Default")),
            SimpleTerm('alexis', 'alexis', _(u"label_alexis", default=u"Alexis")),
        ]))
    slider_gallery_images_preload_type = schema.Choice(
        title=_(u"unitegallery_gallery_images_preload_type_title", default=u"Preload type of the images"),
        description=_(u"unitegallery_gallery_images_preload_type_description", default=u"Minimal - only image nabours will be loaded each time.\nVisible - visible thumbs images will be loaded each time.\nAll - load all the images first time."),
        default=u'minimal',
        vocabulary=SimpleVocabulary([
            SimpleTerm('minimal', 'minimal', _(u"label_minimal", default=u"Minimal")),
            SimpleTerm('visible', 'visible', _(u"label_visible", default=u"Visible")),
            SimpleTerm('all', 'all', _(u"label_all", default=u"All")),
        ]))
    slider_gallery_pause_on_mouseover = schema.Bool(
        title=_(u"unitegallery_gallery_pause_on_mouseover_title", default=u"Pause on mouseover when playing slideshow"),
        default=True)
    slider_gallery_control_thumbs_mousewheel = schema.Bool(
        title=_(u"unitegallery_gallery_control_thumbs_mousewheel_title", default=u"Enable / disable the mousewheel"),
        default=False)
    slider_gallery_control_keyboard = schema.Bool(
        title=_(u"unitegallery_gallery_control_keyboard_title", default=u"Enable / disble keyboard controls"),
        default=True)
    slider_gallery_carousel = schema.Bool(
        title=_(u"unitegallery_gallery_carousel_title", default=u"Next button on last image goes to first image"),
        default=True)
    slider_gallery_preserve_ratio = schema.Bool(
        title=_(u"unitegallery_gallery_preserve_ratio_title", default=u"Preserver ratio when on window resize"),
        default=True)
    slider_gallery_debug_errors = schema.Bool(
        title=_(u"unitegallery_gallery_debug_errors_title", default=u"Show error message when there is some error on the gallery area"),
        default=True)
    slider_gallery_background_color = schema.TextLine(
        title=_(u"unitegallery_gallery_background_color_title", default=u"Set custom background color. If not set it will be taken from css"),
        default=u'',
        required=False)


class UniteGallerySliderType(UniteGalleryCommon):
    """Unite Gallery Default"""
    name = u"unitegallery-slider"
    description = _('Unite Gallery Slider')
    theme = 'slider'
    schema = IUniteGallerySliderSettings


UniteGallerySliderSettings = createSettingsFactory(UniteGallerySliderType.schema)

