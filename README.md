# LeitorLivre

Leitor de tela open source para Windows, escrito em Python. A versão 0.1 oferece leitura da janela ativa, consulta do elemento em foco, síntese de voz offline, atalho global e preferências salvas em JSON.

## Requisitos

- Windows 11
- Python 3.14.6
- Inno Setup 7.1.0 (o build também reconhece Inno Setup 6)
- Tkinter, incluído na instalação padrão do Python para Windows
- Dependências listadas em `requirements.txt`

## Instalação e execução

Abra o PowerShell na pasta do projeto:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

## Funcionalidades da versão 0.1

- Ler janela atual
- Atalho Insert+T
- Falar ao iniciar
- Ajustar velocidade da voz
- Salvar preferências

## Build e instalador para Windows

Com Python 3.14.6 e Inno Setup 7.1.0 instalados, dê duplo clique em `compilar.bat` ou execute-o na raiz do projeto:

```powershell
.\compilar.bat
```

O script cria o ambiente isolado `.venv-build` usando `py -3.14`, confere que a versão selecionada é exatamente 3.14.6, instala as dependências, gera o executável com PyInstaller e procura `ISCC.exe` no PATH ou nas pastas comuns do Inno Setup 7/6. Se uma dependência falhar, a mensagem será exibida no terminal.

Arquivos esperados:

- Executável: `dist\LeitorLivre\LeitorLivre.exe`
- Instalador: `dist\installer\LeitorLivre-Setup-0.1.0.exe`

## Observações

O programa consulta localmente o título da janela ativa e informações acessíveis do controle em foco. Não envia esses dados pela rede.
