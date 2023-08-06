from plone.app.standardtiles.contentlisting import ContentListingTile, DefaultQuery as baseDefaultQuery, DefaultSortOn as baseDefaultSortOn
from plone.app.z3cform.widget import QueryStringFieldWidget
from plone.autoform.directives import widget
from zope.interface import implementer
from zope.component import adapter
from plone.app.imaging.interfaces import IImageScaling
from plone.supermodel import model
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.form.interfaces import IValue
from z3c.form.util import getSpecification
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import queryUtility, getMultiAdapter
from zope.publisher.browser import BrowserView
from zope.schema import getFields
from zope import schema
from plone.tiles import Tile
from plone.tiles.interfaces import ITileType
from collective.tiles.unitegallery import _
from Products.CMFPlone import PloneMessageFactory as _pmf

class IUnitegalleryTile(model.Schema):
    """Unite Gallery Tile schema"""

# NOT working in plone.app.tiles 3.0.0
#    model.fieldset(
#        'default',
#        label=_pmf(u"Default"),
#        fields=['query', 'sort_on', 'sort_reversed', 'limit', 'gallery_theme', 'gallery_skin']
#    )

    widget(query=QueryStringFieldWidget)
    query = schema.List(
        title=_(u"Search terms"),
        value_type=schema.Dict(value_type=schema.Field(),
                               key_type=schema.TextLine()),
        description=_(u"Define the search terms for the items "
                      u"you want to list by choosing what to match on. The "
                      u"list of results will be dynamically updated"),
        required=False
    )

    sort_on = schema.TextLine(
        title=_(u'label_sort_on', default=u'Sort on'),
        description=_(u"Sort the collection on this index"),
        required=False,
    )

    sort_reversed = schema.Bool(
        title=_(u'label_sort_reversed', default=u'Reversed order'),
        description=_(u'Sort the results in reversed order'),
        required=False,
    )

    limit = schema.Int(
        title=_(u'Limit'),
        description=_(u'Limit Search Results'),
        required=False,
        default=100,
        min=1,
    )


    gallery_theme = schema.Choice(
        title=_(u"gallery_theme_title", default=u"Unite Gallery Theme"),
        default=u'default',
        vocabulary=SimpleVocabulary([
            SimpleTerm('default', 'default', _(u"label_default", default=u"Default")),
            SimpleTerm('carousel', 'carousel', _(u"label_carousel", default=u"Carousel")),
            SimpleTerm('compact', 'compact', _(u"label_compact", default=u"Compact")),
            SimpleTerm('grid', 'grid', _(u"label_grid", default=u"Grid")),
            SimpleTerm('slider', 'slider', _(u"label_slider", default=u"Slider")),
            SimpleTerm('tiles', 'tiles', _(u"label_tiles", default=u"Tiles")),
            SimpleTerm('tilesgrid', 'tilesgrid', _(u"label_tilesgrid", default=u"Tiles Grid")),
            SimpleTerm('video', 'video', _(u"label_video", default=u"Video")),
        ]))

    gallery_skin = schema.Choice(
        title=_(u"gallery_skin_title", default=u"The global skin of the gallery"),
        description=_(u"gallery_skin_description", default=u"Will change all gallery items by default"),
        default=u'default',
        vocabulary=SimpleVocabulary([
            SimpleTerm('default', 'default', _(u"label_default", default=u"Default")),
            SimpleTerm('alexis', 'alexis', _(u"label_alexis", default=u"Alexis")),
        ]))
    gallery_play_interval = schema.Int(
        title=_(u"gallery_play_interval_title", default=u"Play interval of the slideshow"),
        default=3000)
    gallery_pause_on_mouseover = schema.Bool(
        title=_(u"gallery_pause_on_mouseover_title", default=u"Pause on mouseover when playing slideshow"),
        default=True)
    gallery_width = schema.TextLine(
        title=_(u"gallery_width_title", default=u"Gallery width"),
        default=u'100%')
    gallery_height = schema.Int(
        title=_(u"gallery_height_title", default=u"Gallery height"),
        default=500)
    gallery_min_width = schema.Int(
        title=_(u"gallery_min_width_title", default=u"Gallery minimal width when resizing"),
        default=400)
    gallery_min_height = schema.Int(
        title=_(u"gallery_min_height_title", default=u"Gallery minimal height when resizing"),
        default=300)
    gallery_images_preload_type = schema.Choice(
        title=_(u"gallery_images_preload_type_title", default=u"Preload type of the images"),
        description=_(u"gallery_images_preload_type_description", default=u"Minimal - only image nabours will be loaded each time.\nVisible - visible thumbs images will be loaded each time.\nAll - load all the images first time."),
        default=u'minimal',
        vocabulary=SimpleVocabulary([
            SimpleTerm('minimal', 'minimal', _(u"label_minimal", default=u"Minimal")),
            SimpleTerm('visible', 'visible', _(u"label_visible", default=u"Visible")),
            SimpleTerm('all', 'all', _(u"label_all", default=u"All")),
        ]))
    gallery_control_thumbs_mousewheel = schema.Bool(
        title=_(u"gallery_control_thumbs_mousewheel_title", default=u"Enable / disable the mousewheel"),
        default=False)

    tiles_type = schema.Choice(
        title=_(u"tiles_type_title", default=u"Must option for the tiles"),
        default=u'columns',
        vocabulary=SimpleVocabulary([
            SimpleTerm('columns', 'columns', _(u"label_columns", default=u"Columns")),
            SimpleTerm('justified', 'justified', _(u"label_justified", default=u"Justified")),
            SimpleTerm('nested', 'nested', _(u"label_nested", default=u"Nested")),
        ]))

    tiles_type_windowswitch = schema.Int(
        title=_(u"tiles_type_windowswitch_title", default=u"Window width to swith between columns and nested"),
        description=_(u"tiles_type_windowswitch_description", default=u"Gallery will be loaded as justified if window width is less than this value."),
        default=0)

    tile_enable_textpanel = schema.Bool(
        title=_(u"tile_enable_textpanel_title", default=u"Enable textpanel"),
        default=False)
    
    slider_transition = schema.Choice(
        title=_(u"slider_transition_title", default=u"Transition of the slide change"),
        default=u'slide',
        vocabulary=SimpleVocabulary([
            SimpleTerm('fade', 'fade', _(u"label_fade", default=u"Fade")),
            SimpleTerm('slide', 'slide', _(u"label_slide", default=u"Slide")),
        ]))
    slider_transition_speed = schema.Int(
        title=_(u"slider_transition_speed_title", default=u"Transition duration of slide change"),
        default=300)
    slider_control_zoom = schema.Bool(
        title=_(u"slider_control_zoom_title", default=u"enable zooming control"),
        default=True)


@implementer(IValue)
@adapter(None, None, None, getSpecification(IUnitegalleryTile['query']), None)  # noqa
class DefaultQuery(baseDefaultQuery):
    """Default Query"""
    
@implementer(IValue)
@adapter(None, None, None, getSpecification(IUnitegalleryTile['sort_on']), None)  # noqa
class DefaultSortOn(baseDefaultSortOn):
    """Default Sort On"""

def jsbool(val):
    if val:
        return 'true'
    return 'false'

class UnitegalleryTile(Tile):
    """Unite Gallery Tile"""

    slidertypes = ['default', 'compact', 'grid', 'slider']

    def getUID(self):
        return self.request.get('URL').split('/')[-1]

    @property
    def theme(self):
        theme = self.data.get('gallery_theme', 'default')
        if not theme:
            return 'default'
        return theme

    def theme_js_url(self):
        return '++resource++ptg.unitegallery/themes/'+self.theme+'/ug-theme-'+self.theme+'.js'

    def theme_css(self):
        if self.theme != 'default':
            return ''
        return """
<link rel="stylesheet" type="text/css"
    href="++resource++ptg.unitegallery/themes/%(theme)s/ug-theme-%(theme)s.css" media="screen" />
""" % {
    'theme':self.theme,
    }
        
    def skin_css(self):
        skin = self.data.get('gallery_skin', 'default')
        if skin == 'default':
            return ''
        return """
<link rel="stylesheet" type="text/css"
    href="++resource++ptg.unitegallery/skins/%(skin)s/%(skin)s.css" media="screen" />
""" % {
    'skin':skin,
    }

    def css(self):
        return u"""
<link rel="stylesheet" type="text/css"
    href="%(base_url)s/css/unite-gallery.css" media="screen" />
%(theme_css)s
%(skin_css)s
""" % {
        'staticFiles': self.staticFiles,
        'base_url': self.typeStaticFiles,
        'theme_css' : self.theme_css(),
        'skin_css' : self.skin_css(),
        }

    @property
    def gallery_width(self):
        width = ''
        if self.theme != 'video':
            width = self.data.get('gallery_width', '100%')
            try:
                width = str(int(width))
            except:
                width = '"'+width+'"'
            return 'gallery_width: '+width+','
        return width
    
    @property
    def gallery_height(self):
        height = ''
        if self.theme in self.slidertypes:
            height = self.data.get('gallery_height', '500')
            try:
                height = str(int(height))
            except:
                height = '"'+height+'"'
            return 'gallery_height: '+height+','
        return ''


    @property
    def gallery_min_width(self):
        width = ''
        if self.theme != 'video':
            width = self.data.get('gallery_min_width', '900')
            try:
                width = str(int(width))
            except:
                width = '"'+width+'"'
            return 'gallery_min_width: '+width+','
        return width
    
    @property
    def gallery_min_height(self):
        height = ''
        if self.theme in self.slidertypes:
            height = self.data.get('gallery_min_height', '500')
            try:
                height = str(int(height))
            except:
                height = '"'+height+'"'
            return 'gallery_min_height: '+height+','
        return height
    
    @property
    def slider_transition_speed(self):
        speed = ''
        if self.theme in self.slidertypes:
            speed = str(self.data.get('slider_transition_speed', 500))
            return 'slider_transition_speed: '+speed+','
        return speed

    @property
    def tiles_type_var(self):
        if not self.theme == 'tiles':
            return '""'
        tiles_type = self.data.get('tiles_type', 'columns')
        if self.data.get('tiles_type_windowswitch'):
            windowswitch = str(self.data.get('tiles_type_windowswitch'))
            return '$(window).width() < '+windowswitch+' ? "justified" : "'+self.data.get('tiles_type', 'columns')+'"'
        return '"'+tiles_type+'"'

    @property
    def tiles_type(self):
        if not self.theme == 'tiles':
            return ''
        return 'tiles_type: tiles_type,'
    
    def script(self):
        theme = self.data.get('gallery_theme', 'default')
        return """
<script type="text/javascript">
var gallery%(uid)s;
requirejs(["tiles-unitegallery"], function(util) {
    requirejs(["%(theme_js_url)s"], function(util) {
        (function($){
            $(document).ready(function() {
                if ($('body').hasClass('template-edit')) return;
                $("#gallery%(uid)s").each(function(){
                    var tiles_type = %(tiles_type_var)s;
                    gallery%(uid)s = $(this).unitegallery({
                            %(gallery_theme)s
                            %(tiles_type)s
                            %(gallery_play_interval)s
                            %(gallery_width)s
                            %(gallery_height)s
                            %(gallery_min_width)s
                            %(gallery_min_height)s
                            %(gallery_min_width)s
                            %(gallery_images_preload_type)s
                            %(gallery_control_thumbs_mousewheel)s
                            %(gallery_pause_on_mouseover)s
                            %(tile_enable_textpanel)s
                            %(slider_transition)s
                            %(slider_transition_speed)s
                            %(slider_control_zoom)s
                        });
			        });
			    });
        })(jQuery);
    });
});
</script>
""" % {'uid':self.getUID(),
       'theme_js_url':self.theme_js_url(),
       'gallery_theme':self.theme != 'default' and 'gallery_theme: "'+self.theme+'",' or '',
       'tiles_type':self.tiles_type,
       'tiles_type_var':self.tiles_type_var,
       'gallery_play_interval':self.theme in self.slidertypes and 'gallery_play_interval: '+str(self.data.get('gallery_play_interval'))+',' or '',
       'gallery_width':self.gallery_width,
       'gallery_height':self.gallery_height,
       'gallery_min_width':self.gallery_min_width,
       'gallery_min_height':self.gallery_min_height,
       'gallery_images_preload_type':self.theme in self.slidertypes and 'gallery_images_preload_type: "'+self.data.get('gallery_images_preload_type', 'minimal')+'",' or '',
       'gallery_control_thumbs_mousewheel':self.theme in self.slidertypes and 'gallery_control_thumbs_mousewheel: '+jsbool(self.data.get('gallery_control_thumbs_mousewheel'))+',' or '',
       'gallery_pause_on_mouseover':self.theme in self.slidertypes and 'gallery_pause_on_mouseover: '+jsbool(self.data.get('gallery_pause_on_mouseover'))+',' or '',
       'slider_transition':self.theme in self.slidertypes and 'slider_transition: "'+str(self.data.get('slider_transition'))+'",' or '',
       'slider_transition_speed':self.slider_transition_speed,
       'slider_control_zoom':self.theme in self.slidertypes and 'slider_control_zoom: '+jsbool(self.data.get('slider_control_zoom'))+',' or '',
       'tile_enable_textpanel':self.theme in ['tiles', 'tilesgrid', 'carousel'] and 'tile_enable_textpanel: '+jsbool(self.data.get('tile_enable_textpanel', 'true'))+',' or '',
       }


    def tag(self, img, fieldname=None, scale=None, height=None, width=None,
            css_class=None, direction='keep', data={}, **args):

        if scale is not None:
            available = self.getAvailableSizes(fieldname)
            if scale not in available:
                return None
            width, height = available[scale]

        if width is None and height is None:
            field = self.field(fieldname)
            return field.tag(
                self.context, css_class=css_class, **args
            )

        info = self.getInfo(
            fieldname=fieldname, scale=scale,
            height=height, width=width,
            direction=direction,
        )

        width = info['width']
        height = info['height']
        mimetype = info['mimetype']
        extension = mimetype.split('/')[-1]

        url = self.context.absolute_url()
        src = '%s/@@images/%s.%s' % (url, info['uid'], extension)
        result = '<img src="%s"' % src

        if height:
            result = '%s height="%s"' % (result, height)

        if width:
            result = '%s width="%s"' % (result, width)

        if css_class is not None:
            result = '%s class="%s"' % (result, css_class)

        if data:
            for key, value in sorted(data.items()):
                if value:
                    result = '%s %s="%s"' % (result, key, value)
        if args:
            for key, value in sorted(args.items()):
                if value:
                    result = '%s %s="%s"' % (result, key, value)

        return '%s />' % result

    def contents(self):
        self.query = self.data.get('query')
        self.sort_on = self.data.get('sort_on')

        if self.query is None or self.sort_on is None:
            # Get defaults
            tileType = queryUtility(ITileType, name=self.__name__)
            fields = getFields(tileType.schema)
            if self.query is None:
                self.query = getMultiAdapter((
                    self.context,
                    self.request,
                    None,
                    fields['query'],
                    None
                ), name="default").get()
            if self.sort_on is None:
                self.sort_on = getMultiAdapter((
                    self.context,
                    self.request,
                    None,
                    fields['sort_on'],
                    None
                ), name="default").get()

        self.limit = self.data.get('limit')
        if self.data.get('sort_reversed'):
            self.sort_order = 'reverse'
        else:
            self.sort_order = 'ascending'
        """Search results"""
        builder = getMultiAdapter(
            (self.context, self.request), name='querybuilderresults'
        )
        accessor = builder(
            query=self.query,
            sort_on=self.sort_on or 'getObjPositionInParent',
            sort_order=self.sort_order,
            limit=self.limit
        )
        return accessor

    def tags(self):
        out = []
        for item in self.contents():
            img = item.getObject()
            image = getMultiAdapter((img, self.request), name='images')
            data = {'data-title':item.Title().decode('utf-8'),
                    'data-description':item.Description().decode('utf-8'),
                    'data-image':item.getURL()}
            tag = image.tag(scale='preview')[:-2]
            for key, value in sorted(data.items()):
                if value:
                    tag = '%s %s="%s"' % (tag, key, value)
            tag = '%s />' % tag
            out.append(tag)
        return out

