import gzip, base64

import pystac
import re
from pathlib import Path
from scour import scour


def minify_svg(svg: str, digits: int = 3) -> str:
    o = scour.sanitizeOptions()
    o.digits = digits               # coordinate precision
    o.strip_xml_prolog = True
    o.remove_metadata = True
    o.strip_comments = True
    o.shorten_ids = True
    o.enable_viewboxing = True
    o.indent_type = "none"
    o.newlines = False
    return scour.scourString(svg, o)


def pack(svg: str) -> str:
    return base64.b64encode(gzip.compress(svg.encode(), 9)).decode()


def read_svg(f_svg: Path) -> str:
    """path -> clean inline SVG string ."""

    svg = f_svg.read_text(encoding="utf-8")
    svg = re.sub(r"<\?xml.*?\?>|<!DOCTYPE.*?>", "", svg, flags=re.S).strip()
    svg = minify_svg(svg)

    # make it scale with its container
    return svg.replace("<svg", '<svg style="max-width:100%;height:auto"', 1)


def path_svg(item) -> str:
    """stac item -> path"""

    # href
    href = Path(item.get_self_href())

    f_svg = href.parent / item.assets['threshold_diagram'].href

    # make it scale with its container
    return f_svg


def path(items: list[pystac.item.Item]):
    '''
    read threshold diagram svg images
    '''

    p_svg = []

    # loop through items
    for item in items:
        p_svg.append(path_svg(item))

    return p_svg