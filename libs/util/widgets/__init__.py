# coding=utf-8
from django.forms.widgets import RadioSelect, RadioFieldRenderer
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms import RadioSelect

class ButtonRadioSelect(RadioSelect):
    class ButtonRadioInput(RadioSelect):
        def __unicode__(self): return self.render()
        def render(self, name=None, value=None, attrs=None, choices=()):
            name = name or self.name
            value = value or self.value
            attrs = attrs or self.attrs
            if 'id' in self.attrs:
                label_for = ' for="%s_%s"' % (self.attrs['id'], self.index)
            else:
                label_for = ''
            choice_label = conditional_escape(force_unicode(self.choice_label))
            return mark_safe(u'%s <label class="titulo04 set01" %s>%s</label>' % (self.tag(), label_for, choice_label))

    class ButtonRadioFieldRenderer(RadioFieldRenderer):
        def __iter__(self):
            for i, choice in enumerate(self.choices):
                yield ButtonRadioSelect.ButtonRadioInput(self.name, self.value, self.attrs.copy(), choice, i)

        def __getitem__(self, idx):
            choice = self.choices[idx]
            # Let the IndexError propogate
            return ButtonRadioSelect.ButtonRadioInput(self.name, self.value, self.attrs.copy(), choice, idx)

        def render(self):
            # return mark_safe(u'<ul class="form-button-radio">\n%s\n</ul>' % u'\n'.join([u'<li>%s</li>' % force_unicode(w) for w in self]))
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

    renderer = ButtonRadioFieldRenderer