# coding=utf-8
from django.contrib.admin import site
from django.contrib import admin

from libs.util.forms import ZModelAdmin
from .models import Cupom, CupomMassa
from django.conf import settings
import copy
from django.contrib import messages
from django.shortcuts import redirect


@admin.register(CupomMassa)
class CupomMassaAdmin(admin.ModelAdmin):
    list_display = ['title', 'data_limite']


class CupomAdmin(ZModelAdmin):
    class Media:
        js = ('%sjs/cps.js' % settings.STATIC_URL,)

    list_display = ['tipo', 'codigo', 'cliente', 'valor_desconto', 'percentual_desconto', 'qte_max_uso', 'qte_usada', 'data_limite', 'ativo']
    raw_id_fields = ['cliente', 'produtos']
    list_filter = ['tipo', 'ativo', 'data_limite']
    search_fields = ['codigo', 'cliente__nome', 'produtos__nome']

    fieldsets = [
        (None, {
            'fields': ('tipo', 'codigo', 'qte_max_uso', 'primeira_compra', 'ativo', 'data_limite',
                       'produtos')
        }),
        ('Cliente(s)', {
            'classes': ('cliente',),
            'fields': ('cliente',),
        }),
        ('Valor', {
            'classes': ('valor',),
            'fields': ('valor_desconto',),
        }),
        ('Percentual', {
            'classes': ('percent',),
            'fields': ('percentual_desconto',)
        }),
    ]

    def _copy(self, request, pk):
        cupom = Cupom.objects.get(pk=pk)
        cupom_cp = copy.copy(cupom)
        cupom_cp.id = None
        cupom_cp.tipo = cupom.tipo
        cupom_cp.codigo = None
        cupom_cp.qte_max_uso = cupom.qte_max_uso
        cupom_cp.primeira_compra = cupom.primeira_compra
        cupom_cp.ativo = cupom.ativo
        cupom_cp.data_limite = cupom.data_limite
        cupom_cp.valor_desconto = cupom.valor_desconto
        cupom_cp.percentual_desconto = cupom.percentual_desconto

        cupom_cp.save()
        # Add produtos
        for produto in cupom.produtos.all():
            cupom_cp.produtos.add(produto)

        messages.success(request, u"Cupom {}, Duplicado com sucesso.".format(cupom_cp.codigo))
        return redirect('/admin/cupom/cupom/%d/' % cupom_cp.id)

    def response_change(self, request, obj):
        if request.POST.get("_copy"):
            return self._copy(request, obj.id)
        return super(CupomAdmin, self).response_change(request, obj)


site.register(Cupom, CupomAdmin)