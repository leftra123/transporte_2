from django import forms
from .models import Transporte, Escuela, Oferente, Chofer

class TransporteForm(forms.ModelForm):
    escuela_set = forms.ModelMultipleChoiceField(
        queryset=Escuela.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    chofer = forms.ModelChoiceField(
        queryset=Chofer.objects.all(),
        widget=forms.Select,
        required=True
    )

    class Meta:
        model = Transporte
        fields = ('patente', 'oferente', 'chofer', 'cantidad_km', 'alumnos', 'sectores', 'escuela_set', 'url_mapa')

    def __init__(self, *args, **kwargs):
        super(TransporteForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['escuela_set'].initial = self.instance.escuela.all()

    def save(self, *args, **kwargs):
        instance = super(TransporteForm, self).save(commit=False)
        instance.save()
        instance.escuela.set(self.cleaned_data['escuela_set'])
        return instance


     

class EscuelaForm(forms.ModelForm):
    class Meta:
        model = Escuela
        fields = '__all__'
        widgets = {
            'rbd': forms.NumberInput(attrs={'class': 'form-control'}),
            'digito_verificador': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'rbd': 'RBD',
            'digito_verificador': 'Dígito Verificador',
            'nombre': 'Nombre',
        }

class OferenteForm(forms.ModelForm):
    class Meta:
        model = Oferente
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre',
            'rut': 'RUT',
        }

class ChoferForm(forms.ModelForm):
    class Meta:
        model = Chofer
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'oferente': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre',
            'rut': 'RUT',
            'oferente': 'Oferente',
        }
