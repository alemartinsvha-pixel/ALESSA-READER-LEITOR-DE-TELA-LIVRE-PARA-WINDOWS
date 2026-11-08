"""Síntese de voz offline com processamento em uma thread dedicada."""

from __future__ import annotations

import logging
from queue import Queue
from threading import Thread
from typing import Final


_LOGGER = logging.getLogger(__name__)
_STOP: Final = object()


class VoiceEngine:
    """Gerencia a fila de mensagens e o mecanismo pyttsx3."""

    def __init__(self, rate: int = 180) -> None:
        self._queue: Queue[object] = Queue()
        self._rate = self._validar_velocidade(rate)
        self._thread = Thread(
            target=self._worker,
            name="LeitorLivreVoice",
            daemon=True,
        )
        self._thread.start()

    @staticmethod
    def _validar_velocidade(rate: int) -> int:
        """Limita a velocidade a um intervalo razoável."""
        return max(80, min(350, int(rate)))

    def speak(self, text: str) -> None:
        """Adiciona uma mensagem à fila de fala."""
        mensagem = str(text).strip()
        if mensagem:
            self._queue.put(("speak", mensagem))

    def set_rate(self, rate: int) -> None:
        """Atualiza a velocidade da fala na thread de voz."""
        self._rate = self._validar_velocidade(rate)
        self._queue.put(("rate", self._rate))

    def stop(self) -> None:
        """Solicita o encerramento da thread de voz."""
        if self._thread.is_alive():
            self._queue.put(_STOP)
            self._thread.join(timeout=3)

    def _worker(self) -> None:
        """Inicializa e usa o pyttsx3 fora da thread da interface."""
        try:
            import pyttsx3

            engine = pyttsx3.init()
            engine.setProperty("rate", self._rate)
            _LOGGER.info("Mecanismo pyttsx3 inicializado.")
        except Exception:
            _LOGGER.exception("Não foi possível inicializar pyttsx3.")
            return

        while True:
            item = self._queue.get()

            if item is _STOP:
                break

            try:
                comando, valor = item

                if comando == "rate":
                    engine.setProperty("rate", int(valor))
                    _LOGGER.info("Velocidade da voz alterada para %s.", valor)
                elif comando == "speak":
                    engine.say(str(valor))
                    engine.runAndWait()
            except Exception:
                _LOGGER.exception("Erro ao processar uma operação de voz.")

        try:
            engine.stop()
        except Exception:
            _LOGGER.exception("Erro ao finalizar o mecanismo de voz.")
