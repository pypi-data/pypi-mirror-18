from . import UniteGalleryCommon
from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.i18nmessageid import MessageFactory
from zope import schema
from collective.plonetruegallery.interfaces import IBaseSettings
from collective.plonetruegallery.browser.views.display import jsbool
_ = MessageFactory('collective.ptg.unitegallery')


class IUniteGalleryDefaultSettings(IBaseSettings):

    #Theme options
    default_theme_enable_fullscreen_button = schema.Bool(
        title=_(u"unitegallery_theme_enable_fullscreen_button_title", default=u"Theme fullscreen button"),
	    description=_(u"unitegallery_theme_enable_fullscreen_button_description",
	        default=u"show, hide the theme fullscreen button. The position in the theme is constant"),
        default=True)
    default_theme_enable_play_button = schema.Bool(
        title=_(u"unitegallery_theme_enable_play_button_title", default=u"Theme play button"),
	    description=_(u"unitegallery_theme_enable_play_button_description",
	        default=u"show, hide the theme play button. The position in the theme is constant"),
        default=True)
    default_theme_enable_hidepanel_button = schema.Bool(
        title=_(u"unitegallery_theme_enable_hidepanel_button_title", default=u"Theme hidepanel button"),
	    description=_(u"unitegallery_theme_enable_hidepanel_button_description",
	        default=u"show, hide the hidepanel button"),
        default=True)
    default_theme_enable_text_panel = schema.Bool(
        title=_(u"unitegallery_theme_enable_text_panel_title", default=u"Enable the panel text panel"),
        default=True)
    default_theme_text_padding_left = schema.Int(
        title=_(u"unitegallery_theme_text_padding_left_title", default=u"Left padding of the text in the textpanel"),
        default=20)
    default_theme_text_padding_right = schema.Int(
        title=_(u"unitegallery_theme_text_padding_right_title", default=u"Right padding of the text in the textpanel"),
        default=5)
    default_theme_text_align = schema.Choice(
        title=_(u"unitegallery_theme_text_align_title", default=u"The align of the text in the textpanel"),
        default='left',
        vocabulary=SimpleVocabulary([
            SimpleTerm('left', 'left', _(u"label_left", default=u"Left")),
            SimpleTerm('center', 'center', _(u"label_center", default=u"Center")),
            SimpleTerm('right', 'right', _(u"label_right", default=u"Right")),
        ]))
    default_theme_text_type = schema.Choice(
        title=_(u"unitegallery_theme_text_type_title", default=u"Text that will be shown on the textpanel"),
        default='title',
        vocabulary=SimpleVocabulary([
            SimpleTerm('title', 'title', _(u"label_title", default=u"Title")),
            SimpleTerm('description', 'description', _(u"label_description", default=u"Description")),
        ]))
    default_theme_hide_panel_under_width = schema.Int(
        title=_(u"unitegallery_theme_hide_panel_under_width_title", default=u"Minimal width display panel"),
        description=_(u"unitegallery_theme_hide_panel_under_width_description", default=u"Hide panel under certain browser width, if null, don't hide"),
        default=480)

    #Gallery options
    default_gallery_width = schema.Int(
        title=_(u"unitegallery_gallery_width_title", default=u"Gallery width"),
        default=900)
    default_gallery_height = schema.Int(
        title=_(u"unitegallery_gallery_height_title", default=u"Gallery height"),
        default=500)
    default_gallery_min_width = schema.Int(
        title=_(u"unitegallery_gallery_min_width_title", default=u"Gallery minimal width when resizing"),
        default=400)
    default_gallery_min_height = schema.Int(
        title=_(u"unitegallery_gallery_min_height_title", default=u"Gallery minimal height when resizing"),
        default=300)
    default_gallery_skin = schema.Choice(
        title=_(u"unitegallery_gallery_skin_title", default=u"The global skin of the gallery"),
        description=_(u"unitegallery_gallery_skin_description", default=u"Will change all gallery items by default"),
        default=u'default',
        vocabulary=SimpleVocabulary([
            SimpleTerm('default', 'default', _(u"label_default", default=u"Default")),
            SimpleTerm('alexis', 'alexis', _(u"label_alexis", default=u"Alexis")),
        ]))
    default_gallery_images_preload_type = schema.Choice(
        title=_(u"unitegallery_gallery_images_preload_type_title", default=u"Preload type of the images"),
        description=_(u"unitegallery_gallery_images_preload_type_description", default=u"Minimal - only image nabours will be loaded each time.\nVisible - visible thumbs images will be loaded each time.\nAll - load all the images first time."),
        default=u'minimal',
        vocabulary=SimpleVocabulary([
            SimpleTerm('minimal', 'minimal', _(u"label_minimal", default=u"Minimal")),
            SimpleTerm('visible', 'visible', _(u"label_visible", default=u"Visible")),
            SimpleTerm('all', 'all', _(u"label_all", default=u"All")),
        ]))
    default_gallery_pause_on_mouseover = schema.Bool(
        title=_(u"unitegallery_gallery_pause_on_mouseover_title", default=u"Pause on mouseover when playing slideshow"),
        default=True)
    default_gallery_control_thumbs_mousewheel = schema.Bool(
        title=_(u"unitegallery_gallery_control_thumbs_mousewheel_title", default=u"Enable / disable the mousewheel"),
        default=False)
    default_gallery_control_keyboard = schema.Bool(
        title=_(u"unitegallery_gallery_control_keyboard_title", default=u"Enable / disble keyboard controls"),
        default=True)
    default_gallery_carousel = schema.Bool(
        title=_(u"unitegallery_gallery_carousel_title", default=u"Next button on last image goes to first image"),
        default=True)
    default_gallery_preserve_ratio = schema.Bool(
        title=_(u"unitegallery_gallery_preserve_ratio_title", default=u"Preserver ratio when on window resize"),
        default=True)
    default_gallery_debug_errors = schema.Bool(
        title=_(u"unitegallery_gallery_debug_errors_title", default=u"Show error message when there is some error on the gallery area"),
        default=True)
    default_gallery_background_color = schema.TextLine(
        title=_(u"unitegallery_gallery_background_color_title", default=u"Set custom background color. If not set it will be taken from css"),
        default=u'',
        required=False)
					
    #Thumb options
    default_thumb_round_corners_radius = schema.Int(
        title=_(u"unitegallery_thumb_round_corners_radius_title", default=u"Thumb border radius"),
        default=0)
    default_thumb_color_overlay_effect = schema.Bool(
	    title=_(u"unitegallery_thumb_color_overlay_effect_title", default=u"Thumb color overlay effect"),
	    description=_(u"unitegallery_thumb_color_overlay_effect_description",
	        default=u"thumb color overlay effect, release the overlay on mouseover and selected states"),
	    default=True)
    default_thumb_overlay_color = schema.TextLine(
	    title=_(u"unitegallery_thumb_overlay_color_title", default=u"Thumb overlay color"),
	    default=u"#000000")	
    default_thumb_overlay_opacity = schema.Float(
	    title=_(u"unitegallery_thumb_overlay_opacity_title", default=u"Thumb overlay color opacity"),
	    default=0.4)
    default_thumb_overlay_reverse = schema.Bool(
	    title=_(u"unitegallery_thumb_overlay_reverse_title", default=u"Reverse the overlay, will be shown on selected state only"),
	    default=False)
    default_thumb_image_overlay_effect = schema.Bool(
	    title=_(u"unitegallery_thumb_image_overlay_effect_title", default=u"Images overlay effect on normal state only"),
	    default=False)
    default_thumb_image_overlay_type = schema.Choice(
        title=_(u"unitegallery_thumb_image_overlay_type_title", default=u"Image effect overlay"),
        default=u'bw',
        vocabulary=SimpleVocabulary([
            SimpleTerm('bw', 'bw', _(u"label_black_and_white", default=u"Black and white")),
            SimpleTerm('blur', 'blur', _(u"label_blur", default=u"Blur")),
            SimpleTerm('sepia', 'sepia', _(u"label_sepia", default=u"Sepia")),
        ]))


class UniteGalleryDefaultType(UniteGalleryCommon):
    """Unite Gallery Default"""
    name = u"unitegallery-default"
    theme = 'default'
    description = 'Unite Gallery Default'
    schema = IUniteGalleryDefaultSettings

UniteGalleryDefaultSettings = createSettingsFactory(UniteGalleryDefaultType.schema)
