from django import forms

class ExcelForm(forms.Form):
    archivo_excel = forms.FileField()
    archivo_excel = forms.FileField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}))
