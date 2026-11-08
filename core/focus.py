"""Monitoramento da janela ativa e do elemento em foco."""

from __future__ import annotations

import logging
from threading import Event, Thread
from typing import Callable

from core.accessibility import get_active_window, get_focused_element
from core.config import AppConfig


_LOGGER = logging.getLogger(__name__)


class FocusMonitor:
    """Anuncia mudanças de janela e de elemento em foco."""

    def __init__(
        self,
        speak: Callable[[str], None],
        config: AppConfig,
    ) -> None:
        self._speak = speak
        self._config = config
        self._stop_event = Event()
        self._thread: Thread | None = None

    def start(self) -> None:
        """Inicia o monitoramento em segundo plano."""
        if self._thread and self._thread.is_alive():
            return

        self._stop_event.clear()
        self._thread = Thread(
            target=self._run,
            name="LeitorLivreFocusMonitor",
            daemon=True,
        )
        self._thread.start()
        _LOGGER.info("Monitoramento de foco iniciado.")

    def stop(self) -> None:
        """Solicita o encerramento do monitoramento."""
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)
        _LOGGER.info("Monitoramento de foco encerrado.")

    def _run(self) -> None:
        """Verifica periodicamente se a janela ou o foco mudaram."""
        ultima_janela: str | None = None
        ultimo_foco: tuple[str, str] | None = None

        while not self._stop_event.is_set():
            try:
                janela = get_active_window()
                titulo = janela.title.strip()

                if ultima_janela is None:
                    ultima_janela = titulo
                elif (
                    self._config.monitor_active_window
                    and titulo
                    and titulo != ultima_janela
                ):
                    self._speak(f"Janela: {titulo}")
                    ultima_janela = titulo
                else:
                    ultima_janela = titulo

                if self._config.monitor_focus:
                    elemento = get_focused_element()
                    if elemento:
                        foco_atual = (elemento.name, elemento.control_type)

                        if (
                            ultimo_foco is not None
                            and foco_atual != ultimo_foco
                            and elemento.name
                        ):
                            descricao = elemento.name
                            if elemento.control_type:
                                descricao = (
                                    f"{elemento.control_type}: {descricao}"
                                )
                            self._speak(f"Foco: {descricao}")

                        ultimo_foco = foco_atual
            except Exception:
                _LOGGER.exception("Erro durante o monitoramento de foco.")

            intervalo = max(100, int(self._config.poll_interval_ms))
            self._stop_event.wait(intervalo / 1000)
