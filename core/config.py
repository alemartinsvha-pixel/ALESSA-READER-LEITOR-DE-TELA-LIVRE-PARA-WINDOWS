"""Carregamento e persistência das preferências em JSON."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import logging
import os
from pathlib import Path
import sys
from typing import Any


_LOGGER = logging.getLogger(__name__)

USER_DATA_DIR = (
    Path(os.environ["APPDATA"]) / "LeitorLivre"
    if os.environ.get("APPDATA")
    else Path.home() / "AppData" / "Roaming" / "LeitorLivre"
)
CONFIG_PATH = USER_DATA_DIR / "config.json"


def _caminho_config_padrao() -> Path:
    """Localiza o JSON padrão, tanto no código-fonte quanto no pacote."""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / "data" / "config.json"
    return Path(__file__).resolve().parent.parent / "data" / "config.json"


@dataclass
class AppConfig:
    """Preferências do LeitorLivre."""

    speak_on_start: bool = True
    voice_rate: int = 180
    monitor_active_window: bool = True
    monitor_focus: bool = True
    poll_interval_ms: int = 400

    def save(self, path: Path = CONFIG_PATH) -> None:
        """Salva as preferências usando substituição atômica do arquivo."""
        path.parent.mkdir(parents=True, exist_ok=True)
        arquivo_temporario = path.with_suffix(".tmp")

        with arquivo_temporario.open("w", encoding="utf-8") as arquivo:
            json.dump(asdict(self), arquivo, ensure_ascii=False, indent=2)
            arquivo.write("\n")

        arquivo_temporario.replace(path)
        _LOGGER.info("Configuração salva em %s.", path)


def _validar_int(
    valor: Any,
    padrao: int,
    minimo: int,
    maximo: int,
) -> int:
    """Converte e limita um valor numérico inteiro."""
    try:
        convertido = int(valor)
    except (TypeError, ValueError):
        return padrao

    return max(minimo, min(maximo, convertido))


def _config_a_partir_de(dados: Any) -> AppConfig:
    """Cria a configuração a partir de um objeto JSON."""
    if not isinstance(dados, dict):
        raise ValueError("A configuração deve ser um objeto JSON.")

    padrao = AppConfig()

    return AppConfig(
        speak_on_start=bool(
            dados.get("speak_on_start", padrao.speak_on_start)
        ),
        voice_rate=_validar_int(
            dados.get("voice_rate", padrao.voice_rate),
            padrao.voice_rate,
            minimo=80,
            maximo=350,
        ),
        monitor_active_window=bool(
            dados.get(
                "monitor_active_window",
                padrao.monitor_active_window,
            )
        ),
        monitor_focus=bool(
            dados.get("monitor_focus", padrao.monitor_focus)
        ),
        poll_interval_ms=_validar_int(
            dados.get("poll_interval_ms", padrao.poll_interval_ms),
            padrao.poll_interval_ms,
            minimo=100,
            maximo=5000,
        ),
    )


def load_config(path: Path | None = None) -> AppConfig:
    """Carrega as preferências do usuário ou cria o arquivo inicial."""
    destino = path or CONFIG_PATH

    if not destino.exists():
        try:
            caminho_padrao = _caminho_config_padrao()
            if caminho_padrao.exists():
                with caminho_padrao.open("r", encoding="utf-8") as arquivo:
                    config = _config_a_partir_de(json.load(arquivo))
            else:
                config = AppConfig()
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            _LOGGER.exception(
                "Não foi possível ler a configuração padrão; "
                "serão usados os valores internos."
            )
            config = AppConfig()

        config.save(destino)
        return config

    try:
        with destino.open("r", encoding="utf-8") as arquivo:
            return _config_a_partir_de(json.load(arquivo))
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        _LOGGER.exception(
            "Configuração inválida; as preferências padrão serão usadas."
        )
        config = AppConfig()
        config.save(destino)
        return config
