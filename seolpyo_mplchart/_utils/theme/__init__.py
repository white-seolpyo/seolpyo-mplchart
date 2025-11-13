from typing import Literal

from ..._config import ConfigData, SliderConfigData

from . import light, dark


def set_theme(config: ConfigData|SliderConfigData, theme: Literal['light', 'dark']='dark'):
    if theme == 'light':
        config = light.set_theme(config)
    elif theme == 'dark':
        config = dark.set_theme(config)

    return config

