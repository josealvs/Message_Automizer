from django.shortcuts import render
from .forms import UploadArquivoForm
from .utils import processar_planilha

def upload_planilha(request):
    if request.method == 'POST':
        form = UploadArquivoForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = request.FILES['arquivo']
            contatos_enviados = processar_planilha(arquivo)
            return render(request, 'mensagens/sucesso.html', {'contatos': contatos_enviados})
    else:
        form = UploadArquivoForm()
    return render(request, 'mensagens/upload.html', {'form': form})

