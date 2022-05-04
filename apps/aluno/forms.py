# -*- coding: utf-8 -*-
# Autor: christian
from django import forms
from django.forms import ModelForm
from django_localflavor_br import br_states

from .models import Aluno
from .models import verificar_email


# Create the form class.
class AlunoForm(ModelForm):
    class Meta:
        _estados = (('', '---'),) + br_states.STATE_CHOICES
        model = Aluno
        exclude = ['termo', 'usuario', 'data_cadastro', 'newsletter']
        widgets = {
                'sexo': forms.Select(attrs={'class': 'form-control'}),
                'nome': forms.TextInput(attrs={'class': 'form-control'}),
                'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
                'cpf': forms.TextInput(attrs={'class': 'form-control', 'data-mask': '999.999.999-99'}),
                'rg': forms.TextInput(attrs={'class': 'form-control'}),
                # CONTATO
                'email': forms.EmailInput(attrs={'class': 'form-control'}),
                'email_publico': forms.CheckboxInput(),
                'cargo': forms.TextInput(attrs={'class': 'form-control'}),
                'frase': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': u'Diga algo sobre você para a comunidade JusTutor'
                }),

            'url_facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'url_flicker': forms.URLInput(attrs={'class': 'form-control'}),
            'url_twitter': forms.URLInput(attrs={'class': 'form-control'}),
            'url_instagram': forms.URLInput(attrs={'class': 'form-control'}),

            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'data-mask': '(99)99999-9999'}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'data-mask': '(99)99999-9999'}),
            # CONTATO
            'cep': forms.TextInput(
                attrs={'class': 'form-control', 'data-mask': '99999-999',
                       'onchange': "Dajaxice.apps.aluno.get_cep(Dajax.process, {'cep': $('#id_cep').val()});block()"
                       }),
            'logradouro': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'uf': forms.Select(attrs={'class': 'form-control'}, choices=_estados),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'termo': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'newsletter': forms.CheckboxInput(attrs={'class': 'form-control'})
        }


class CadastroAlunoForm(forms.Form):
    # _estados = (('', '---'),) + br_states.STATE_CHOICES
    # DADOS GERAIS
    # sexo = forms.CharField(
    #     widget=forms.RadioSelect(choices=[('M', 'Masculino'), ('F', 'Feminino')])
    # )
    # foto = forms.ImageField(
    #     # widget=forms.RadioSelect(choices=[('M', 'Masculino'), ('F', 'Feminino')])
    # )
    nome = forms.CharField(
        max_length=150, min_length=3, widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    # cpf = BRCPFField(
    #     widget=forms.TextInput(attrs={'class': 'form-control', 'data-mask': '999.999.999-99'})
    # )
    # rg = forms.CharField(
    #     required=False, widget=forms.TextInput(attrs={'class': 'form-control'})
    # )
    # CONTATO
    email = forms.EmailField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        min_length=6, widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        min_length=6, widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    # telefone = forms.CharField(
    #     required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'data-mask': '(99)?999999999'})
    # )
    # celular = forms.CharField(
    #     required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'data-mask': '(99)?999999999'})
    # )
    # # CONTATO
    # cep = BRZipCodeField(
    #     required=False, widget=forms.TextInput(
    #         attrs={'class': 'form-control', 'data-mask': '99999-999',
    #                'onchange': "Dajaxice.apps.aluno.get_cep(Dajax.process, {'cep': $('#id_cep').val()});block()"
    #                })
    # )
    # logradouro = forms.CharField(
    #     required=False, widget=forms.TextInput(attrs={'class': 'form-control'})
    # )
    # numero = forms.CharField(
    #     required=False, max_length=5, widget=forms.TextInput(attrs={'class': 'form-control'})
    # )
    # bairro = forms.CharField(
    #     required=False, widget=forms.TextInput(attrs={'class': 'form-control'})
    # )
    # complemento = forms.CharField(
    #     required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'})
    # )
    # uf = forms.CharField(
    #      required=False, widget=forms.Select(attrs={'class': 'form-control'}, choices=_estados)
    # )
    # cidade = forms.CharField(
    #     required=False, widget=forms.TextInput(attrs={'class': 'form-control'})
    # )
    # newsletter = forms.BooleanField(
    #     label=u"Gostaria de receber no seu e-mail novidades, notícias e promoções especiais.",
    #     required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'})
    # )
    termo = forms.BooleanField(
        required=True, widget=forms.CheckboxInput(attrs={'class': 'form-control'})
    )
    newsletter = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super(CadastroAlunoForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        email = cleaned_data.get('email')

        if password != password2:
            self.add_error('password2', 'As senhas não conferem.')

        if verificar_email(email):
            self.add_error('email', 'Já existe um Usuário cadastrado com esse e-mail.')


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Nome')
    last_name = forms.CharField(max_length=30, label='Sobrenome')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
    #
    # def validate_unique_email(self, value):
    #     print '>>>> VALIDATE', value
    #
    # def save(self, request):
    #     print '>>>> SAVE', request
