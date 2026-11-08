# LeitorLivre

Leitor de tela open source para Windows, escrito em Python. A versão 0.1 oferece leitura da janela ativa, consulta do elemento em foco, síntese de voz offline, atalho global e preferências salvas em JSON.

## Requisitos

- Windows 11
- Python 3.15.x (o script seleciona essa versão com `py -3.15` quando disponível)
- Inno Setup 7.1.0 (o build também reconhece Inno Setup 6)
- Tkinter, incluído na instalação padrão do Python para Windows
- Dependências listadas em `requirements.txt`

## Instalação e execução

Abra o PowerShell na pasta do projeto:

```powershell
py -3.15 -m venv .venv
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

Com Python 3.15.x e Inno Setup instalados, dê um duplo clique em `compilar.bat`, ou execute na raiz do projeto:

```powershell
.\compilar.bat
```

O arquivo chama `build.ps1`, que confere a versão Python, instala as dependências de build, compila com PyInstaller e localiza `ISCC.exe` via PATH ou nos diretórios padrão do Inno Setup 7/6. A compilação só será concluída se a versão do PyInstaller disponível no PyPI for compatível com o Python instalado.

Arquivos esperados:

- Executável: `dist\LeitorLivre\LeitorLivre.exe`
- Instalador: `dist\installer\LeitorLivre-Setup-0.1.0.exe`

## Estrutura

```text
LeitorLivre/
├── main.py
├── core/
├── gui/
├── data/
├── logs/
├── requirements.txt
├── requirements-build.txt
├── build.ps1
├── compilar.bat
├── build/LeitorLivre.spec
└── installer/LeitorLivre.iss
```

## Observações

O programa consulta localmente o título da janela ativa e informações acessíveis do controle em foco. Não envia esses dados pela rede.
