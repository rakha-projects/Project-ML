"""Embed chart bytes so they do not depend on Streamlit's media URLs."""
from __future__ import annotations

import base64
from html import escape


def png_markup(data: bytes, description: str) -> str:
    """Build a responsive, accessible PNG that is sent with the page itself."""
    if not data.startswith(b'\x89PNG\r\n\x1a\n'):
        raise ValueError('Grafik harus berupa gambar PNG.')
    encoded = base64.b64encode(data).decode('ascii')
    return (
        '<figure style="margin:0;width:100%">'
        f'<img src="data:image/png;base64,{encoded}" '
        f'alt="{escape(description, quote=True)}" '
        'style="display:block;width:100%;height:auto;max-width:100%">'
        '</figure>'
    )
