from django import forms
from .models import Transporte, Escuela

class TransporteForm(forms.ModelForm):
    escuela_set = forms.ModelMultipleChoiceField(
        queryset=Escuela.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Transporte
        fields = ('patente', 'oferente', 'cantidad_km', 'alumnos', 'sectores', 'escuela_set', 'url_mapa')

    def __init__(self, *args, **kwargs):
        super(TransporteForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['escuela_set'].initial = self.instance.escuela.all()

    def save(self, *args, **kwargs):
        instance = super(TransporteForm, self).save(commit=False)
        instance.save()
        instance.escuela.set(self.cleaned_data['escuela_set'])
        return instance

# class TransporteForm(forms.ModelForm):
#     class Meta:
#         model = Transporte
#         fields = '__all__'
#         widgets = {
#             'patente': forms.TextInput(attrs={'class': 'form-control'}),
#             'oferente': forms.TextInput(attrs={'class': 'form-control'}),
#             'cantidad_km': forms.NumberInput(attrs={'class': 'form-control'}),
#             'alumnos': forms.NumberInput(attrs={'class': 'form-control'}),
#             'sectores': forms.TextInput(attrs={'class': 'form-control'}),
#             'escuela': forms.Select(attrs={'class': 'form-select'}),
#             'url_mapa': forms.URLInput(attrs={'class': 'form-control'}),
#         }
#         labels = {
#             'patente': 'Patente',
#             'oferente': 'Oferente',
#             'cantidad_km': 'Cantidad de KM',
#             'alumnos': 'Alumnos',
#             'sectores': 'Sectores',
#             'escuela': 'Escuela',
#             'url_mapa': 'URL del mapa'
#         }

        

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
