"""Aplicação principal do LeitorLivre."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
import tkinter as tk
from tkinter import ttk

from core.accessibility import get_active_window, get_focused_element
from core.config import AppConfig, USER_DATA_DIR, load_config
from core.focus import FocusMonitor
from core.voice import VoiceEngine
from gui.settings_window import SettingsWindow


LOG_DIR = USER_DATA_DIR / "logs"
LOG_FILE = LOG_DIR / "leitor_livre.log"


def configurar_logs() -> None:
    """Configura o log rotativo na pasta de dados do usuário."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
    )

    logging.basicConfig(
        level=logging.INFO,
        handlers=[handler],
        force=True,
    )


class LeitorLivreApp:
    """Coordena a interface, a voz, os atalhos e o monitoramento."""

    def __init__(self, root: tk.Tk, config: AppConfig) -> None:
        self.root = root
        self.config = config
        self.logger = logging.getLogger(__name__)

        self.root.title("LeitorLivre")
        self.root.geometry("440x270")
        self.root.minsize(380, 240)
        self.root.protocol("WM_DELETE_WINDOW", self.encerrar)

        self.voice = VoiceEngine(rate=self.config.voice_rate)
        self.monitor = FocusMonitor(
            speak=self.voice.speak,
            config=self.config,
        )

        self.hotkey_handle = None
        self.keyboard_module = None

        self._criar_interface()
        self._registrar_atalho()
        self.monitor.start()

        if self.config.speak_on_start:
            self.voice.speak("LeitorLivre iniciado.")

        self.logger.info("LeitorLivre iniciado.")

    def _criar_interface(self) -> None:
        """Monta a janela principal do programa."""
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="LeitorLivre",
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w")

        ttk.Label(
            frame,
            text="Leitor de tela open source para Windows",
        ).pack(anchor="w", pady=(2, 14))

        ttk.Label(
            frame,
            text="Atalho para ler a janela atual: Insert+T",
        ).pack(anchor="w", pady=(0, 12))

        botoes = ttk.Frame(frame)
        botoes.pack(fill="x")

        ttk.Button(
            botoes,
            text="Ler janela atual",
            command=self.ler_janela_atual,
        ).pack(side="left")

        ttk.Button(
            botoes,
            text="Configurações",
            command=self.abrir_configuracoes,
        ).pack(side="left", padx=(8, 0))

        ttk.Button(
            botoes,
            text="Sair",
            command=self.encerrar,
        ).pack(side="right")

        self.status_var = tk.StringVar(value="Monitoramento ativo.")
        ttk.Label(
            frame,
            textvariable=self.status_var,
            foreground="#444444",
        ).pack(anchor="w", pady=(18, 0))

    def _registrar_atalho(self) -> None:
        """Registra Insert+T como atalho global."""
        try:
            import keyboard

            self.keyboard_module = keyboard
            self.hotkey_handle = keyboard.add_hotkey(
                "insert+t",
                self.ler_janela_atual,
                trigger_on_release=True,
                suppress=False,
            )
            self.logger.info("Atalho global Insert+T registrado.")
        except Exception:
            self.logger.exception(
                "Não foi possível registrar o atalho global Insert+T."
            )
            self.status_var.set(
                "Atalho indisponível. Use o botão para ler a janela."
            )

    def ler_janela_atual(self) -> None:
        """Lê o título da janela ativa e, se disponível, o foco atual."""
        try:
            janela = get_active_window()
            partes = []

            if janela.title:
                partes.append(f"Janela atual: {janela.title}")
            else:
                partes.append("Não foi possível identificar a janela ativa.")

            elemento = get_focused_element()
            if elemento and elemento.name:
                descricao = elemento.name
                if elemento.control_type:
                    descricao = f"{elemento.control_type}: {descricao}"
                partes.append(f"Elemento em foco: {descricao}")

            mensagem = ". ".join(partes)
            self.voice.speak(mensagem)
            self.logger.info("Leitura manual solicitada: %s", mensagem)

            self.root.after(
                0,
                lambda: self.status_var.set("Leitura da janela solicitada."),
            )
        except Exception:
            self.logger.exception("Falha ao ler a janela atual.")
            self.voice.speak("Não foi possível ler a janela atual.")

    def abrir_configuracoes(self) -> None:
        """Abre a janela de configurações."""
        SettingsWindow(
            parent=self.root,
            config=self.config,
            on_save=self._salvar_configuracoes,
        )

    def _salvar_configuracoes(self) -> None:
        """Persiste as preferências e aplica a velocidade de voz."""
        try:
            self.config.save()
            self.voice.set_rate(self.config.voice_rate)
            self.logger.info("Preferências salvas.")
            self.status_var.set("Preferências salvas.")
        except OSError:
            self.logger.exception("Não foi possível salvar as preferências.")
            self.status_var.set("Erro ao salvar as preferências.")

    def encerrar(self) -> None:
        """Finaliza os componentes da aplicação."""
        self.logger.info("Encerrando o LeitorLivre.")

        try:
            self.monitor.stop()
        except Exception:
            self.logger.exception("Erro ao parar o monitor de foco.")

        if self.keyboard_module and self.hotkey_handle is not None:
            try:
                self.keyboard_module.unhook(self.hotkey_handle)
            except Exception:
                self.logger.exception("Erro ao remover o atalho global.")

        try:
            self.voice.stop()
        except Exception:
            self.logger.exception("Erro ao encerrar o mecanismo de voz.")

        self.root.destroy()


def main() -> None:
    configurar_logs()
    logger = logging.getLogger(__name__)

    try:
        config = load_config()
        root = tk.Tk()
        LeitorLivreApp(root, config)
        root.mainloop()
    except Exception:
        logger.exception("Erro fatal ao iniciar o LeitorLivre.")
        raise


if __name__ == "__main__":
    main()
