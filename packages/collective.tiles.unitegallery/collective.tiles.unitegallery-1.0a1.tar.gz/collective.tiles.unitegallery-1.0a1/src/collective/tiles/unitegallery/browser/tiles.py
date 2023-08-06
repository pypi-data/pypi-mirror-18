from plone.app.standardtiles.contentlisting import ContentListingTile, DefaultQuery as baseDefaultQuery, DefaultSortOn as baseDefaultSortOn
from plone.app.z3cform.widget import QueryStringFieldWidget
from plone.autoform.directives import widget
from zope.interface import implementer
from zope.component import adapter
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

    tiles_type = schema.Choice(
        title=_(u"tiles_type_title", default=u"Must option for the tiles"),
        default=u'columns',
        vocabulary=SimpleVocabulary([
            SimpleTerm('columns', 'columns', _(u"label_columns", default=u"Columns")),
            SimpleTerm('justified', 'justified', _(u"label_justified", default=u"Justified")),
            SimpleTerm('nested', 'nested', _(u"label_nested", default=u"Nested")),
        ]))

    tile_enable_textpanel = schema.Bool(
        title=_(u"tile_enable_textpanel_title", default=u"Enable textpanel"),
        default=False)


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
        if self.theme in ['default', 'compact', 'grid', 'slicer']:
            height = self.data.get('gallery_height', '500')
            try:
                height = str(int(height))
            except:
                height = '"'+height+'"'
            return 'gallery_height: '+height+','
        return height


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
        if self.theme in ['default', 'compact', 'grid', 'slicer']:
            height = self.data.get('gallery_min_height', '500')
            try:
                height = str(int(height))
            except:
                height = '"'+height+'"'
            return 'gallery_min_height: '+height+','
        return height 
    
    def script(self):
        theme = self.data.get('gallery_theme', 'default')
        return """
<script type="text/javascript">
requirejs(["tiles-unitegallery"], function(util) {
    requirejs(["%(theme_js_url)s"], function(util) {
        (function($){
            $(document).ready(function() {
                $("#gallery-%(uid)s").each(function(){
                        $(this).unitegallery({
                            %(gallery_theme)s
                            %(tiles_type)s
                            %(gallery_width)s
                            %(gallery_height)s
                            %(gallery_min_width)s
                            %(gallery_min_height)s
                            %(gallery_min_width)s
                            %(gallery_images_preload_type)s
                            %(tile_enable_textpanel)s
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
       'tiles_type':self.theme == 'tiles' and 'tiles_type: "'+self.data.get('tiles_type', 'columns')+'",' or '',
       'gallery_width':self.gallery_width,
       'gallery_height':self.gallery_height,
       'gallery_min_width':self.gallery_min_width,
       'gallery_min_height':self.gallery_min_height,
       'gallery_images_preload_type':self.theme in ['default', 'compact', 'grid','slider'] and 'gallery_images_preload_type: "'+self.data.get('gallery_images_preload_type', 'minimal')+'",' or '',
       'tile_enable_textpanel':self.theme in ['tiles', 'tilesgrid', 'carousel'] and 'tile_enable_textpanel: '+jsbool(self.data.get('tile_enable_textpanel', 'true'))+',' or '',
       }

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


