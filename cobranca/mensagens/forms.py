from django import forms

class UploadArquivoForm(forms.Form):
    arquivo = forms.FileField()
