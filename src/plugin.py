# plugin.py

import re

from pathlib import Path
from mkdocs.plugins import BasePlugin


def modify_match(match):
    caption, image_link, attr_list = match.groups()
    image_link = ('..' / Path(image_link)).as_posix()
    if attr_list:
        attr_list = attr_list.replace('{', '').replace('}', '')
    else:
        attr_list = ''

    return (
        r'<figure class="figure-image">'
        rf'  <img src="{image_link}" alt="{caption}" {attr_list}>'
        rf'  <figcaption>{caption}</figcaption>'
        r'</figure>'
    )


class Image2FigurePlugin(BasePlugin):
    def on_page_markdown(self, markdown, **kwargs):

        pattern = re.compile(r'!\[(.*?)\]\((.*?)\)(\{[^\}]*\})?', flags=re.IGNORECASE)
        markdown = re.sub(pattern, modify_match, markdown)

        return markdown
