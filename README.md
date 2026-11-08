# LeitorLivre

Leitor de tela open source para Windows, escrito em Python. A versão 0.1 oferece leitura da janela ativa, consulta do elemento em foco, síntese de voz offline, atalho global e preferências salvas em JSON.

## Requisitos

- Windows 11
- Python 3.14
- Tkinter, incluído na instalação padrão do Python para Windows
- Dependências listadas em `requirements.txt`

## Instalação

Abra o PowerShell na pasta do projeto:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Execução

```powershell
python main.py
```

## Funcionalidades da versão 0.1

- Ler janela atual
- Atalho Insert+T
- Falar ao iniciar
- Ajustar velocidade da voz
- Salvar preferências

## Estrutura

```text
LeitorLivre/
├── main.py
├── core/
│   ├── voice.py
│   ├── focus.py
│   ├── accessibility.py
│   └── config.py
├── gui/
│   └── settings_window.py
├── data/
│   └── config.json
├── logs/
├── requirements.txt
├── README.md
└── .gitignore
```

## Observações

O programa consulta localmente o título da janela ativa e informações acessíveis do controle em foco. Não envia esses dados pela rede.
