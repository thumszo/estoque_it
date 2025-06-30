from django import forms
from .models import Item
from .models import Movimento

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['nome', 'categoria', 'quantidade', 'estoque_minimo', 'descricao']

    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get('nome')
        categoria = cleaned_data.get('categoria')

        if nome and categoria:
            # Exclui o próprio item do filtro, se estiver em edição
            itens_duplicados = Item.objects.filter(
                nome__iexact=nome,
                categoria=categoria
            )
            if self.instance.pk:
                itens_duplicados = itens_duplicados.exclude(pk=self.instance.pk)

            if itens_duplicados.exists():
                raise forms.ValidationError("Este item já está cadastrado com essa categoria.")

        return cleaned_data

class MovimentoForm(forms.ModelForm):
    class Meta:
        model = Movimento
        fields = ['item', 'tipo', 'quantidade']
