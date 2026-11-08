# LeitorLivre

Leitor de tela open source para Windows, escrito em Python. A versão 0.1 oferece leitura da janela ativa, consulta do elemento em foco, síntese de voz offline, atalho global e preferências salvas em JSON.

## Requisitos

- Windows 11
- Python 3.15.2
- Inno Setup 7.1.0
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

Com Python 3.15.2 e Inno Setup instalados, dê duplo clique em `compilar.bat`, ou execute na raiz do projeto:

```powershell
.\compilar.bat
```

O script cria o ambiente isolado `.venv-build` com `py -3.15`, confere que a versão usada é exatamente 3.15.2, instala/atualiza as dependências e o PyInstaller, gera o executável e procura `ISCC.exe` no PATH ou nos locais padrão do Inno Setup 7/6. Se a instalação do PyInstaller ou de alguma dependência falhar, leia a mensagem de erro exibida; isso pode indicar incompatibilidade do pacote com Python 3.15.2.

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
