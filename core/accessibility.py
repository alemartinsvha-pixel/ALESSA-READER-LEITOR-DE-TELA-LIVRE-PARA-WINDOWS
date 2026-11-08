"""Acesso ao título da janela ativa e ao elemento de UI Automation em foco."""

from __future__ import annotations

from dataclasses import dataclass
import ctypes
import logging
import os


_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class ActiveWindow:
    """Informações básicas da janela em primeiro plano."""

    handle: int | None
    title: str


@dataclass(frozen=True)
class FocusedElement:
    """Descrição acessível do controle que está em foco."""

    name: str
    control_type: str = ""


def get_active_window() -> ActiveWindow:
    """Obtém o identificador e o título da janela ativa no Windows."""
    if os.name != "nt":
        return ActiveWindow(handle=None, title="Windows não detectado")

    try:
        user32 = ctypes.WinDLL("user32", use_last_error=True)

        user32.GetForegroundWindow.restype = ctypes.c_void_p
        user32.GetWindowTextLengthW.argtypes = [ctypes.c_void_p]
        user32.GetWindowTextLengthW.restype = ctypes.c_int
        user32.GetWindowTextW.argtypes = [
            ctypes.c_void_p,
            ctypes.c_wchar_p,
            ctypes.c_int,
        ]
        user32.GetWindowTextW.restype = ctypes.c_int

        handle = user32.GetForegroundWindow()
        if not handle:
            return ActiveWindow(handle=None, title="Nenhuma janela ativa")

        tamanho = user32.GetWindowTextLengthW(handle)
        buffer = ctypes.create_unicode_buffer(max(tamanho + 1, 2))
        user32.GetWindowTextW(handle, buffer, len(buffer))

        return ActiveWindow(handle=int(handle), title=buffer.value.strip())
    except Exception:
        _LOGGER.exception("Falha ao consultar a janela ativa.")
        return ActiveWindow(handle=None, title="")


def get_focused_element() -> FocusedElement | None:
    """Obtém nome e tipo do elemento acessível que está em foco."""
    if os.name != "nt":
        return None

    try:
        import uiautomation as automation

        control = automation.GetFocusedControl()
        if control is None:
            return None

        nome = str(getattr(control, "Name", "") or "").strip()
        tipo = str(getattr(control, "ControlTypeName", "") or "").strip()

        return FocusedElement(name=nome, control_type=tipo)
    except Exception:
        _LOGGER.debug(
            "Não foi possível consultar o elemento em foco.",
            exc_info=True,
        )
        return None
