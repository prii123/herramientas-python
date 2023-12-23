from django import forms

class ExcelFormConciliacion(forms.Form):
    archivo_bancos = forms.FileField()
    archivo_bancos = forms.FileField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}))

    archivo_contable = forms.FileField()
    archivo_contable = forms.FileField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}))