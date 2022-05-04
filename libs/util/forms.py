from django.contrib import messages
from django.contrib.admin import ModelAdmin
from django.forms import ModelForm, HiddenInput, Form
from django.shortcuts import render, redirect

class ZForm(Form):
    def __init__(self, *args, **kwargs):
        super(ZForm, self).__init__(*args, **kwargs)
        for field in self.required_fields: self.fields[field].required = True
        for field in self.hidden_fields: self.fields[field].widget = HiddenInput()
        try:
            for field, widget in self.custom_widgets.items(): self.fields[field].widget = widget
        except: pass
        for field, value in self.initial_values.items(): self.fields[field].initial = value
        for field, value in self.help_text.items(): self.fields[field].help_text = value
        if self.all_fields_properties:
            for field in self.fields:
                for k,v in self.all_fields_properties.items():
                    self.fields[field].widget.attrs.update({k:v})
        if self.required_depends and self.data:
            for campo in self.required_depends:
                for k,v in self.required_depends[campo].items():
                    try:
                        if self.data[campo] == k:
                            for i in v:
                                self.fields[i].required = True
                    except: pass
        for field in self.fields_properties:
            for k, v in self.fields_properties[field].items():
                self.fields[field].widget.attrs.update({k:v})
        if self.all_fields_classes:
            for field in self.fields:
                self.fields[field].widget.attrs.update({'class':u'%s %s'%(self.fields[field].widget.attrs.get('class') or '', self.all_fields_classes)})
        for item in self.fields_classes:
            self.fields[item[0]].widget.attrs.update({'class':u'%s %s'%(self.fields[item[0]].widget.attrs.get('class') or '', item[1])})

        if self.placeholder:
            for field in self.fields:
                self.fields[field].widget.attrs['placeholder'] = self.fields[field].label

    required_fields                 = []
    required_depends                = {}
    fields_properties               = {}
    fields_classes                  = {}
    all_fields_properties           = {}
    all_fields_classes              = ''
    custom_widgets                  = {}
    initial_values                  = {}
    hidden_fields                   = []
    help_text                       = {}
    placeholder                     = False
    _instance                       = None
    _form                           = None
    template                        = None
    def run(self, request, template=None, *args, **kwargs):
        self.template               = template
        self._instance              = kwargs.get('instance', None)
        self._form = self.__class__(request.POST or None, request.FILES or None, instance=kwargs.get('instance') or None, )
        if self._form.is_valid():
            if 'save' in kwargs and not kwargs['save']: return self
            else:
                self._instance = self._form.save()
                self.alert(request, **kwargs)
                if 'redirect' in kwargs: return redirect(kwargs['redirect'])
        return self._return(request, template, self._form, **kwargs)

    def go(self, request, template, form, **kwargs):
        self.alert(request, **kwargs)
        return render(request, template, {'form': form})

    def alert(self, request, **kwargs):
        if 'msg' in kwargs: messages.add_message(request, messages.SUCCESS, kwargs['msg'])

    def _return(self, request, template, form, **kwargs):
        kwargs.update({'form': form})
        return render(request, template, kwargs)

class ZModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ZModelForm, self).__init__(*args, **kwargs)
        for field in self.required_fields: self.fields[field].required = True
        for field in self.hidden_fields: self.fields[field].widget = HiddenInput()
        try:
            for field, widget in self.custom_widgets.items(): self.fields[field].widget = widget
        except: pass
        for field, value in self.initial_values.items(): self.fields[field].initial = value
        for field, value in self.help_text.items(): self.fields[field].help_text = value
        if self.all_fields_properties:
            for field in self.fields:
                for k,v in self.all_fields_properties.items():
                    self.fields[field].widget.attrs.update({k:v})
        if self.required_depends and self.data:
            for campo in self.required_depends:
                for k,v in self.required_depends[campo].items():
                    try:
                        if self.data[campo] == k:
                            for i in v:
                                self.fields[i].required = True
                    except: pass
        for field in self.fields_properties:
            for k, v in self.fields_properties[field].items():
                self.fields[field].widget.attrs.update({k:v})
        if self.all_fields_classes:
            for field in self.fields:
                self.fields[field].widget.attrs.update({'class':u'%s %s'%(self.fields[field].widget.attrs.get('class') or '', self.all_fields_classes)})
        for item in self.fields_classes:
            self.fields[item[0]].widget.attrs.update({'class':u'%s %s'%(self.fields[item[0]].widget.attrs.get('class') or '', item[1])})

        if self.placeholder:
            for field in self.fields:
                self.fields[field].widget.attrs['placeholder'] = self.fields[field].label

        if self.item_placeholder:
            for k, v in self.item_placeholder.items():
                self.fields[k].widget.attrs['placeholder'] = v

    required_fields                 = []
    required_depends                = {}
    fields_properties               = {}
    fields_classes                  = {}
    all_fields_properties           = {}
    all_fields_classes              = ''
    custom_widgets                  = {}
    initial_values                  = {}
    hidden_fields                   = []
    help_text                       = {}
    placeholder                     = False
    _instance                       = None
    _form                           = None
    template                        = None
    def run(self, request, template=None, *args, **kwargs):
        self.template               = template
        self._instance              = kwargs.get('instance', None)
        self._form = self.__class__(request.POST or None, request.FILES or None, instance=kwargs.get('instance') or None, )
        if self._form.is_valid():
            if 'save' in kwargs and not kwargs['save']: return self
            else:
                self._instance = self._form.save()
                self.alert(request, **kwargs)
                if 'redirect' in kwargs: return redirect(kwargs['redirect'])
        return self._return(request, template, self._form, **kwargs)

    def go(self, request, template, form, **kwargs):
        self.alert(request, **kwargs)
        return render(request, template, {'form': form})

    def alert(self, request, **kwargs):
        if 'msg' in kwargs: messages.add_message(request, messages.SUCCESS, kwargs['msg'])

    def _return(self, request, template, form, **kwargs):
        kwargs.update({'form': form})
        return render(request, template, kwargs)

class ZModelAdmin(ModelAdmin):
    def __init__(self, *args, **kwargs):
        super(ZModelAdmin, self).__init__(*args, **kwargs)
        if not self.list_display_links: self.list_display_links = self.list_display