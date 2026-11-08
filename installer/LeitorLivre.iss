; Arquivo de instalação do LeitorLivre em Inno Setup

#define MyAppName "LeitorLivre"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "LeitorLivre"
#define MyAppExeName "LeitorLivre.exe"

[Setup]
AppId={{B1A1DF51-911E-41E5-A1DC-5F18B1C0B9DF}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\LeitorLivre
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=..\dist\installer
OutputBaseFilename=LeitorLivre-Setup-{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar um atalho na área de trabalho"; GroupDescription: "Atalhos adicionais:"; Flags: unchecked

[Files]
Source: "..\dist\LeitorLivre\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\LeitorLivre"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\LeitorLivre"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Iniciar o LeitorLivre"; Flags: postinstall nowait skipifsilent
