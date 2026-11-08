"""Janela Tkinter para edição das preferências."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from core.config import AppConfig


class SettingsWindow:
    """Exibe e salva as configurações do LeitorLivre."""

    def __init__(
        self,
        parent: tk.Tk,
        config: AppConfig,
        on_save: Callable[[], None],
    ) -> None:
        self.config = config
        self.on_save = on_save
        self.window = tk.Toplevel(parent)

        self.window.title("Configurações - LeitorLivre")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)

        self.rate_var = tk.IntVar(value=config.voice_rate)
        self.speak_on_start_var = tk.BooleanVar(
            value=config.speak_on_start
        )
        self.monitor_window_var = tk.BooleanVar(
            value=config.monitor_active_window
        )
        self.monitor_focus_var = tk.BooleanVar(
            value=config.monitor_focus
        )

        self._criar_interface()
        self.window.grab_set()

    def _criar_interface(self) -> None:
        """Cria os controles da janela de preferências."""
        frame = ttk.Frame(self.window, padding=18)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Preferências de voz e monitoramento",
            font=("Segoe UI", 11, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        ttk.Label(frame, text="Velocidade da voz:").grid(
            row=1, column=0, sticky="w"
        )
        ttk.Spinbox(
            frame,
            from_=80,
            to=350,
            increment=10,
            textvariable=self.rate_var,
            width=8,
        ).grid(row=1, column=1, sticky="e", padx=(12, 0))

        ttk.Checkbutton(
            frame,
            text="Falar ao iniciar",
            variable=self.speak_on_start_var,
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(12, 0))

        ttk.Checkbutton(
            frame,
            text="Anunciar mudanças de janela ativa",
            variable=self.monitor_window_var,
        ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(6, 0))

        ttk.Checkbutton(
            frame,
            text="Anunciar mudanças do elemento em foco",
            variable=self.monitor_focus_var,
        ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(6, 0))

        botoes = ttk.Frame(frame)
        botoes.grid(row=5, column=0, columnspan=2, sticky="e", pady=(18, 0))

        ttk.Button(
            botoes,
            text="Cancelar",
            command=self.window.destroy,
        ).pack(side="right")

        ttk.Button(
            botoes,
            text="Salvar",
            command=self._salvar,
        ).pack(side="right", padx=(0, 8))

    def _salvar(self) -> None:
        """Atualiza o objeto de configuração e chama o callback."""
        try:
            velocidade = int(self.rate_var.get())
        except (tk.TclError, ValueError):
            velocidade = self.config.voice_rate

        self.config.voice_rate = max(80, min(350, velocidade))
        self.config.speak_on_start = self.speak_on_start_var.get()
        self.config.monitor_active_window = self.monitor_window_var.get()
        self.config.monitor_focus = self.monitor_focus_var.get()

        self.on_save()
        self.window.destroy()
