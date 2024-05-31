from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

import logging

log = logging.getLogger(f"mkdocs.plugins.{__name__}")


class AssetTypeReplacer(BasePlugin):

    def on_page_content(self, html: str, page: Page, config: MkDocsConfig, files: Files) -> str | None:
        if page.url.startswith("api/"):
            log.debug(f"Replacing ASSET_TYPE on {page.url}")
            html = html.replace(
                "ASSET_TYPE", page.title.lower()
            ).replace(
                '<span class="n">asset_type</span><span class="p">,</span>', ""
            )
        return html
