from django import forms
from .models import Item
from .models import Movimento

class ItemForm(forms.ModelForm):  # Formulário para cadastrar ou editar um item do estoque
    class Meta:
        model = Item
        fields = ['nome', 'categoria', 'quantidade', 'estoque_minimo', 'descricao']

    def clean(self):  # Validação personalizada para impedir duplicidade de itens
        cleaned_data = super().clean()
        nome = cleaned_data.get('nome')
        categoria = cleaned_data.get('categoria')

        if nome and categoria:
            # Busca se já existe outro item com o mesmo nome e categoria
            itens_duplicados = Item.objects.filter(
                nome__iexact=nome,
                categoria=categoria
            )
            if self.instance.pk:  # Ignora o próprio item caso esteja editando
                itens_duplicados = itens_duplicados.exclude(pk=self.instance.pk)

            if itens_duplicados.exists():
                raise forms.ValidationError("Este item já está cadastrado com essa categoria.")

        return cleaned_data

class MovimentoForm(forms.ModelForm):  # Formulário para registrar uma movimentação de entrada ou saída de item
    class Meta:
        model = Movimento
        fields = ['item', 'tipo', 'quantidade']
