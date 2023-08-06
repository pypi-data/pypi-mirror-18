import logging
from . import UniteGalleryCommon
from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface
from zope import schema
from collective.plonetruegallery.interfaces import IBaseSettings
_ = MessageFactory('collective.ptg.unitegallery')
LOG = logging.getLogger(__name__)

class IUniteGalleryTilesSettings(IBaseSettings):
    """UniteGallery Tiles Settings"""

    #Theme options
    tiles_theme_enable_preloader = schema.Bool(
        title=_(u"unitegallery_theme_enable_preloader_title", default=u"Enable preloader circle"),
        default=True)
    tiles_theme_preloading_height = schema.Int(
        title=_(u"unitegallery_theme_preloading_height_title", default=u"Preloading height"),
        description=_(u"unitegallery_theme_preloading_height_description", default=u"The height of the preloading div, it show before the gallery"),
        default=200)
    tiles_theme_preloader_vertpos = schema.Int(
        title=_(u"unitegallery_theme_preloader_vertpos_title", default=u"Vertical position of the preloader"),
        default=100)
    tiles_theme_gallery_padding = schema.Int(
        title=_(u"unitegallery_theme_gallery_padding_title", default=u"Horizontal padding of the gallery from the sides"),
        default=0)
    tiles_theme_appearance_order = schema.Choice(
        title=_(u"unitegallery_theme_appearance_order_title", default=u"Appearance order of the tiles"),
        default='normal',
        vocabulary=SimpleVocabulary([
            SimpleTerm('normal', 'normal', _(u"label_normal", default=u"Normal")),
            SimpleTerm('shuffle', 'shuffle', _(u"label_shuffle", default=u"Shuffle")),
            SimpleTerm('keep', 'keep', _(u"label_keep", default=u"Keep")),
        ]))
    tiles_theme_auto_open = schema.Bool(
        title=_(u"unitegallery_theme_auto_open_title", default=u"Auto open lightbox at start"),
        default=False)
    tiles_theme_auto_open_delay = schema.Int(
        title=_(u"unitegallery_theme_auto_open_delay_title", default=u"Delay for auto open lightbox"),
        default=0)

    #Gallery options
    tiles_gallery_width = schema.TextLine(
        title=_(u"unitegallery_gallery_width_title", default=u"Gallery Width"),
        default=u"100%")
    tiles_gallery_min_width = schema.Int(
        title=_(u"unitegallery_gallery_min_width_title", default=u"Gallery minimal width when resizing"),
        default=150)
    tiles_gallery_background_color = schema.TextLine(
        title=_(u"unitegallery_gallery_background_color_title", default=u"Custom background color. If not set it will be taken from css"),
        default=u"",
        required=False)

    #Tiles options
    tiles_tiles_type = schema.Choice(
        title=_(u"unitegallery_tiles_type_title", default=u"Must option for the tiles"),
        default=u'columns',
        vocabulary=SimpleVocabulary([
            SimpleTerm('columns', 'columns', _(u"label_columns", default=u"Columns")),
            SimpleTerm('justified', 'justified', _(u"label_justified", default=u"Justified")),
            SimpleTerm('nested', 'nested', _(u"label_nested", default=u"Nested")),
        ]))
    tiles_tiles_justified_row_height = schema.Int(
        title=_(u"unitegallery_tiles_justified_row_height_title", default=u"Base row height of the justified type"),
        default=150)
    tiles_tiles_justified_space_between = schema.Int(
        title=_(u"unitegallery_tiles_justified_space_between_title", default=u"Space between the tiles justified type"),
        default=3)
    tiles_tiles_nested_optimal_tile_width = schema.Int(
        title=_(u"unitegallery_tiles_nested_optimal_tile_width_title", default=u"Tiles optimal width nested type"),
        default=250)
    tiles_tiles_col_width = schema.Int(
        title=_(u"unitegallery_tiles_col_width_title", default=u"Column width - exact or base according the settings"),
        default=250)
    tiles_tiles_align = schema.Choice(
        title=_(u"unitegallery_tiles_align_title", default=u"Align of the tiles in the space"),
        default=u'center',
        vocabulary=SimpleVocabulary([
            SimpleTerm('center', 'center', _(u"label_center", default=u"Center")),
            SimpleTerm('top', 'top', _(u"label_top", default=u"Top")),
            SimpleTerm('left', 'left', _(u"label_left", default=u"Left")),
            SimpleTerm('right', 'right', _(u"label_right", default=u"Right")),
        ]))
    tiles_tiles_space_between_cols = schema.Int(
        title=_(u"unitegallery_tiles_space_between_cols_title", default=u"Space between images"),
        default=3)
    tiles_tiles_exact_width = schema.Bool(
        title=_(u"unitegallery_tiles_exact_width_title", default=u"Exact width of column - disables the min and max columns"),
        default=False)
    tiles_tiles_space_between_cols_mobile = schema.Int(
        title=_(u"unitegallery_tiles_space_between_cols_mobile_title", default=u"Space between cols for mobile type"),
        default=3)
    tiles_tiles_include_padding = schema.Bool(
        title=_(u"unitegallery_tiles_include_padding_title", default=u"Include padding"),
        description=_(u"unitegallery_tiles_include_padding_description", default=u"Include padding at the sides of the columns, equal to current space between cols"),
        default=True)
    tiles_tiles_min_columns = schema.Int(
        title=_(u"unitegallery_tiles_min_columns_title", default=u"Min columns"),
        default=2)
    tiles_tiles_max_columns = schema.Int(
        title=_(u"unitegallery_tiles_max_columns_title", default=u"Max columns (0 for unlimited)"),
        default=20)
    tiles_tiles_set_initial_height = schema.Bool(
        title=_(u"unitegallery_tiles_set_initial_height_title", default=u"Set initial height, columns type related only"),
        default=True)
    tiles_tiles_enable_transition = schema.Bool(
        title=_(u"unitegallery_tiles_enable_transition_title", default=u"Enable transition when screen width change"),
        default=True)

    #Tile design options
    tiles_tile_enable_border = schema.Bool(
        title=_(u"unitegallery_tile_enable_border_title", default=u"Enable border of the tile"),
        default=False)
    tiles_tile_border_width = schema.Int(
        title=_(u"unitegallery_tile_border_width_title", default=u"Tile border width"),
        default=3)
    tiles_tile_border_color = schema.TextLine(
        title=_(u"unitegallery_tile_border_color_title", default=u"Tile border color"),
        default=u"#F0F0F0")
    tiles_tile_border_radius = schema.Int(
        title=_(u"unitegallery_tile_border_radius_title", default=u"Tile border radius (applied to border only, not to outline)"),
        default=0)
					
    tiles_tile_enable_outline = schema.Bool(
        title=_(u"unitegallery_tile_enable_outline_title", default=u"Enable outline of the tile"),
        description=_(u"unitegallery_tile_enable_outline_description", default=u"Works only together with the border"),
        default=False)
    tiles_tile_outline_color = schema.TextLine(
        title=_(u"unitegallery_tile_outline_color_title", default=u"Tile outline color"),
        default=u"#8B8B8B")
					
    tiles_tile_enable_shadow = schema.Bool(
        title=_(u"unitegallery_tile_enable_outline_title", default=u"Enable shadow of the tile"),
        default=False)
    tiles_tile_shadow_h = schema.Int(
        title=_(u"unitegallery_tile_shadow_h_title", default=u"Position of horizontal shadow"),
        default=1)
    tiles_tile_shadow_v = schema.Int(
        title=_(u"unitegallery_tile_shadow_v_title", default=u"Position of vertical shadow"),
        default=1)
    tiles_tile_shadow_blur = schema.Int(
        title=_(u"unitegallery_tile_shadow_blur_title", default=u"Shadow blur"),
        default=3)
    tiles_tile_shadow_spread = schema.Int(
        title=_(u"unitegallery_tile_shadow_spread_title", default=u"Shadow spread"),
        default=2)
    tiles_tile_shadow_color = schema.TextLine(
        title=_(u"unitegallery_tile_shadow_color_title", default=u"Shadow color"),
        default=u"#8B8B8B")
					
    tiles_tile_enable_action = schema.Bool(
        title=_(u"unitegallery_tile_enable_action_title", default=u"Enable tile action on click like lightbox"),
        default=True)
    tiles_tile_as_link = schema.Bool(
        title=_(u"unitegallery_tile_as_link_title", default=u"Act the tile as link, no lightbox will appear"),
        default=False)
    tiles_tile_link_newpage = schema.Bool(
        title=_(u"unitegallery_tile_link_newpage_title", default=u"Open the tile link in new page"),
        default=True)
		
    tiles_tile_enable_overlay = schema.Bool(
        title=_(u"unitegallery_tile_enable_overlay_title", default=u"Enable tile color overlay (on mouseover)"),
        default=True)
    tiles_tile_overlay_opacity = schema.Float(
        title=_(u"unitegallery_tile_overlay_opacity_title", default=u"Tile overlay opacity"),
        default=0.4)
    tiles_tile_overlay_color = schema.TextLine(
        title=_(u"unitegallery_tile_overlay_color_title", default=u"Tile overlay color"),
        default=u"#000000")
					
    tiles_tile_enable_icons = schema.Bool(
        title=_(u"unitegallery_ile_enable_icons_title", default=u"Enable icons in mouseover mode"),
        default=True)
    tiles_tile_show_link_icon = schema.Bool(
        title=_(u"unitegallery_tile_show_link_icon_title", default=u"Show link icon (if the tile has a link)"),
        description=_(u"unitegallery_tile_show_link_icon_description", default=u"In case of tile_as_link this option not enabled"),
        default=False)
    tiles_tile_space_between_icons = schema.Int(
        title=_(u"unitegallery_tile_space_between_icons_title", default=u"Initial space between icons, (on small tiles it may change)"),
        default=26)
    tiles_tile_enable_image_effect = schema.Bool(
        title=_(u"unitegallery_tile_enable_image_effect_title", default=u"Enable tile image effect"),
        default=False)
    tiles_tile_image_effect_type = schema.Choice(
        title=_(u"unitegallery_tile_image_effect_type_title", default=u"Tile effect type"),
        default=u'bw',
        vocabulary=SimpleVocabulary([
            SimpleTerm('bw', 'bw', _(u"label_black_and_white", default=u"Black and white")),
            SimpleTerm('blur', 'blur', _(u"label_blur", default=u"Blur")),
            SimpleTerm('sepia', 'sepia', _(u"label_sepia", default=u"Sepia")),
        ]))
    tiles_tile_image_effect_reverse = schema.Bool(
        title=_(u"unitegallery_tile_image_effect_reverse_title", default=u"Reverse the image, set only on mouseover state"),
        default=False)

    #tile text panel options
    tiles_tile_enable_textpanel = schema.Bool(
        title=_(u"unitegallery_tile_enable_textpanel_title", default=u"Enable textpanel"),
        default=False)
    tiles_tile_textpanel_source = schema.Choice(
        title=_(u"unitegallery_tile_textpanel_source_title", default=u"Source of the textpanel"),
        default=u'title',
        vocabulary=SimpleVocabulary([
            SimpleTerm('title', 'title', _(u"label_title", default=u"Title")),
            SimpleTerm('desc', 'desc', _(u"label_blur", default=u"Description")),
            SimpleTerm('desc_title', 'desc_title', _(u"label_sepia", default=u"Description or Title")),
        ]))
    tiles_tile_textpanel_always_on = schema.Bool(
        title=_(u"unitegallery_tile_textpanel_always_on_title", default=u"Textpanel always visible"),
        default=False)
    tiles_tile_textpanel_appear_type = schema.Choice(
        title=_(u"unitegallery_tile_textpanel_appear_type_title", default=u"Appear type of the textpanel on mouseover"),
        default=u'slide',
        vocabulary=SimpleVocabulary([
            SimpleTerm('slide', 'slide', _(u"label_slide", default=u"Slide")),
            SimpleTerm('fade', 'fade', _(u"label_fade", default=u"Fade")),
        ]))
    tiles_tile_textpanel_position = schema.Choice(
        title=_(u"unitegallery_tile_textpanel_position_title", default=u"Position of the textpanel"),
        default=u'inside_bottom',
        vocabulary=SimpleVocabulary([
            SimpleTerm('inside_bottom', 'inside_bottom', _(u"label_inside_bottom", default=u"Inside bottom")),
            SimpleTerm('inside_top', 'inside_top', _(u"label_inside_top", default=u"Inside top")),
            SimpleTerm('inside_center', 'inside_center', _(u"label_inside_center", default=u"Inside center")),
            SimpleTerm('top', 'top', _(u"label_top", default=u"Top")),
            SimpleTerm('bottom', 'bottom', _(u"label_bottom", default=u"Bottom")),
        ]))
    tiles_tile_textpanel_offset = schema.Int(
        title=_(u"unitegallery_tile_textpanel_offset_title", default=u"Vertical offset of the textpanel"),
        default=0)
    tiles_tile_textpanel_padding_top = schema.Int(
        title=_(u"unitegallery_tile_textpanel_padding_top_title", default=u"Textpanel padding top"),
        default=8)
    tiles_tile_textpanel_padding_bottom = schema.Int(
        title=_(u"unitegallery_tile_textpanel_padding_bottom_title", default=u"Textpanel padding bottom"),
        default=8)
    tiles_tile_textpanel_padding_right = schema.Int(
        title=_(u"unitegallery_tile_textpanel_padding_right_title", default=u"Cut some space for text from right"),
        default=11)
    tiles_tile_textpanel_padding_left = schema.Int(
        title=_(u"unitegallery_tile_textpanel_padding_left_title", default=u"Cut some space for text from left"),
        default=11)
    tiles_tile_textpanel_bg_opacity = schema.Float(
        title=_(u"unitegallery_tile_textpanel_bg_opacity_title", default=u"Textpanel background opacity"),
        default=0.4)
    tiles_tile_textpanel_bg_color = schema.TextLine(
        title=_(u"unitegallery_tile_textpanel_bg_color_title", default=u"Textpanel background color"),
        default=u"#000000")
    tiles_tile_textpanel_bg_css = schema.Text(
        title=_(u"unitegallery_tile_textpanel_bg_css_title", default=u"Textpanel background css"),
        default=u"{}")
    tiles_tile_textpanel_title_color = schema.TextLine(
        title=_(u"unitegallery_tile_textpanel_bg_color_title", default=u"Textpanel title color. if empty - take from css"),
        default=u"",
        required=False)
    tiles_tile_textpanel_title_font_family = schema.TextLine(
        title=_(u"unitegallery_tile_textpanel_title_font_family_title", default=u"Textpanel title font family. if empty - take from css"),
        default=u"",
        required=False)
    tiles_tile_textpanel_title_text_align = schema.TextLine(
        title=_(u"unitegallery_tile_textpanel_title_text_align_title", default=u"Textpanel title text align. if empty - take from css"),
        default=u"",
        required=False)
    tiles_tile_textpanel_title_font_size = schema.TextLine(
        title=_(u"unitegallery_tile_textpanel_title_font_size_title", default=u"Textpanel title font size. if empty - take from css"),
        default=u"",
        required=False)
    tiles_tile_textpanel_title_bold = schema.TextLine(
        title=_(u"unitegallery_tile_textpanel_title_bold_title", default=u"Textpanel title bold. if empty - take from css"),
        default=u"",
        required=False)
    tiles_tile_textpanel_css_title = schema.Text(
        title=_(u"unitegallery_tile_textpanel_css_title_title", default=u"Textpanel additional css of the title"),
        default=u"{}")
    tiles_tile_textpanel_desc_color = schema.TextLine(
        title=_(u"unitegallery_tile_textpanel_desc_color_title", default=u"Textpanel description font family. if empty - take from css"),
        default=u"",
        required=False)
    tiles_tile_textpanel_desc_font_family = schema.TextLine(
        title=_(u"unitegallery_tile_textpanel_desc_font_family_title", default=u"Textpanel description font family. if empty - take from css"),
        default=u"",
        required=False)
    tiles_tile_textpanel_desc_text_align = schema.TextLine(
        title=_(u"unitegallery_tile_textpanel_desc_text_align_title", default=u"Textpanel description text align. if empty - take from css"),
        default=u"",
        required=False)
    tiles_tile_textpanel_desc_font_size = schema.TextLine(
        title=_(u"unitegallery_tile_textpanel_desc_font_size_title", default=u"Textpanel description font size. if empty - take from css"),
        default=u"",
        required=False)
    tiles_tile_textpanel_desc_bold = schema.TextLine(
        title=_(u"unitegallery_tile_textpanel_desc_bold_title", default=u"Textpanel description bold. if empty - take from css"),
        default=u"",
        required=False)
    tiles_tile_textpanel_css_description = schema.Text(
        title=_(u"unitegallery_tile_textpanel_css_description_title", default=u"Textpanel additional css of the description"),
        default=u"{}")


class UniteGalleryTilesType(UniteGalleryCommon):
    """Unite Gallery Tiles"""
    name = u"unitegallery-tiles"
    description = _('Unite Gallery Tiles')
    theme = 'tiles'
    schema = IUniteGalleryTilesSettings
    nullfields = ['tile_textpanel_title_color',
'tile_textpanel_title_font_family',
'tile_textpanel_title_text_align',
'tile_textpanel_title_font_size',
'tile_textpanel_title_bold',
'tile_textpanel_desc_color',
'tile_textpanel_desc_font_family',
'tile_textpanel_desc_text_align',
'tile_textpanel_desc_font_size',
'tile_textpanel_desc_bold']

    def theme_options(self):
        data = super(UniteGalleryTilesType, self).theme_options()
        if data.get('tiles_type') == 'columns':
            del data['tiles_type']
        if self.settings.tiles_theme_auto_open:
            data['theme_auto_open'] = data['theme_auto_open_delay']
            del data['theme_auto_open_delay']
        else:
            del data['theme_auto_open']
            del data['theme_auto_open_delay']
        for k in self.nullfields:
            if not data.get(k):
                data[k] = 'null'
        return data

UniteGalleryTilesSettings = createSettingsFactory(UniteGalleryTilesType.schema)
