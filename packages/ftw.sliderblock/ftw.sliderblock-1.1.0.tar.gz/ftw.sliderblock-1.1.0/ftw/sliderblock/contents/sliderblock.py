from collections import OrderedDict
from ftw.simplelayout import _ as SLPMF
from ftw.simplelayout.browser.actions import DefaultActions
from ftw.sliderblock import _
from ftw.sliderblock.contents.constraints import validate_slick_config
from ftw.sliderblock.contents.interfaces import ISliderBlock
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.content import Container
from plone.directives import form
from zope import schema
from zope.i18n import translate
from zope.interface import alsoProvides
from zope.interface import implements


class ISliderBlockSchema(form.Schema):
    """Slider block for simplelayout
    """

    title = schema.TextLine(
        title=_(u'sliderblock_title_label', default=u'Title'),
        required=True,
    )

    show_title = schema.Bool(
        title=_(u'sliderblock_show_title_label', default=u'Show title'),
        default=True,
        required=False,
    )

    slick_config = schema.Text(
        title=_(u'sliderblock_slick_config_label', default=u'Configuration'),
        description=_(u'sliderblock_slick_config_description',
                      default=u'See http://kenwheeler.github.io/slick/'),
        required=False,
        default=u'{"autoplay": true, "autoplaySpeed": 2000}',
        constraint=validate_slick_config,
    )

    form.order_before(title='*')

alsoProvides(ISliderBlockSchema, IFormFieldProvider)


class SliderBlock(Container):
    implements(ISliderBlock)


class SliderBlockActions(DefaultActions):

    def specific_actions(self):
        return OrderedDict(
            [
                ('upload', {
                    'class': 'upload icon-image-upload',
                    'title': translate(
                        SLPMF(u'label_upload', default=u'Upload'),
                        context=self.request),
                    'href': './sl-ajax-upload-block-view'
                }),

                ('folderContents', {
                    'class': 'icon-folder-contents redirect',
                    'title': translate(
                        _(u'label_show_folder_contents',
                          default=u'Show folder contents'),
                        context=self.request),
                    'href': '/folder_contents'}),
            ]
        )
