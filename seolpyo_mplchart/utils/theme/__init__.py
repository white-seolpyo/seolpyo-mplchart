from typing import Literal

from ...style import Style

from . import light, dark


def set_theme(style: Style, theme: Literal['light', 'dark']='dark'):
    if theme == 'light':
        style = light.set_theme(style)
    elif theme == 'dark':
        style = dark.set_theme(style)

    return style

