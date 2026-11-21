#!/usr/bin/env python3
"""Gera a versão Single File (quine autossuficiente) do Feather Wiki — Whimsigoth."""

from __future__ import annotations

import argparse
import base64
import mimetypes
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "Feather Wiki — Whimsigoth.html"
DEFAULT_OUTPUT = ROOT / "Feather Wiki — Whimsigoth Single File.html"
DEFAULT_CSS = ROOT / "app" / "style.css"
DEFAULT_JS = ROOT / "app" / "app.js"

LINK_S_RE = re.compile(
    r'<link\b(?=[^>]*\bid=["\']?s["\']?)(?=[^>]*\bhref=["\'][^"\']+["\'])[^>]*>',
    re.IGNORECASE,
)
SCRIPT_A_RE = re.compile(
    r'<script\b(?=[^>]*\bid=["\']?a["\']?)(?=[^>]*\bsrc=["\'][^"\']+["\'])[^>]*>\s*</script>',
    re.IGNORECASE,
)
CSS_URL_RE = re.compile(r'url\(\s*(["\']?)([^)"\']+)\1\s*\)')


def inline_css_assets(css: str, css_dir: Path) -> tuple[str, list[str], list[str]]:
    inlined: list[str] = []
    missing: list[str] = []

    def replacer(match: re.Match[str]) -> str:
        raw_url = match.group(2).strip()
        if raw_url.startswith(("data:", "http://", "https://", "//", "#")):
            return match.group(0)

        asset_path = (css_dir / raw_url).resolve()
        if not asset_path.is_file():
            missing.append(raw_url)
            return match.group(0)

        mime_type, _ = mimetypes.guess_type(asset_path.name)
        mime_type = mime_type or "application/octet-stream"
        encoded = base64.b64encode(asset_path.read_bytes()).decode("ascii")
        inlined.append(raw_url)
        return f'url("data:{mime_type};base64,{encoded}")'

    return CSS_URL_RE.sub(replacer, css), inlined, missing


def escape_closing_tag(content: str, tag: str) -> str:
    return re.sub(rf"</({tag})\b", r"<\/\1", content, flags=re.IGNORECASE)


def minify_css(css: str) -> str:
    """Minifica CSS preservando strings, url(...) e seletores descendentes."""
    preserved: list[str] = []

    def stash(match: re.Match[str]) -> str:
        preserved.append(match.group(0))
        return f"__CSS_KEEP_{len(preserved) - 1}__"

    # Preserva strings ("..." / '...') e url(...) antes de mexer em comentários/espaços
    css = re.sub(
        r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|url\(\s*(?:"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[^)\s]+)\s*\)',
        stash,
        css,
    )
    # Remove comentários /* ... */
    css = re.sub(r"/\*[\s\S]*?\*/", "", css)
    # Colapsa espaços e quebras de linha
    css = re.sub(r"\s+", " ", css)
    # Remove espaços desnecessários ao redor de delimitadores seguros (sem remover espaço antes de ":")
    css = re.sub(r"\s*([{};,>~])\s*", r"\1", css)
    css = re.sub(r":\s+", ":", css)
    # Remove ";" redundante antes de "}"
    css = css.replace(";}", "}")
    # Restaura strings e url(...)
    css = re.sub(r"__CSS_KEEP_(\d+)__", lambda m: preserved[int(m.group(1))], css)
    return css.strip()


def minify_html_shell(html: str) -> str:
    """Remove comentários e espaços/quebras de linha entre tags do HTML base."""
    html = re.sub(r"<!--[\s\S]*?-->", "", html)
    html = re.sub(r">\s+<", "><", html)
    return html.strip()


def build_single_file(
    input_html: Path,
    output_html: Path,
    css_path: Path,
    js_path: Path,
    inline_assets: bool = True,
    minify: bool = True,
) -> None:
    html = input_html.read_text(encoding="utf-8")
    css = css_path.read_text(encoding="utf-8")
    js = js_path.read_text(encoding="utf-8").strip()

    inlined_assets: list[str] = []
    missing_assets: list[str] = []
    if inline_assets:
        css, inlined_assets, missing_assets = inline_css_assets(css, css_path.parent)

    if minify:
        html = minify_html_shell(html)
        css = minify_css(css)

    css = escape_closing_tag(css, "style")
    js = escape_closing_tag(js, "script")

    html, css_count = LINK_S_RE.subn(lambda _: f'<style id="s">{css}</style>', html, count=1)
    if css_count == 0:
        raise ValueError('Tag <link id="s" href="..."> não encontrada no HTML de entrada.')

    html, js_count = SCRIPT_A_RE.subn(lambda _: f'<script id="a">{js}</script>', html, count=1)
    if js_count == 0:
        raise ValueError('Tag <script id="a" src="..."></script> não encontrada no HTML de entrada.')

    output_html.write_text(html, encoding="utf-8")

    print(f"Gerado com sucesso: {output_html} ({output_html.stat().st_size:,} bytes)")
    if inlined_assets:
        print(f"Assets embutidos em Base64: {', '.join(inlined_assets)}")
    if missing_assets:
        print(
            "Aviso: assets referenciados no CSS não foram encontrados (mantidos como URL): "
            + ", ".join(missing_assets)
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gera a versão Single File do Feather Wiki — Whimsigoth."
    )
    parser.add_argument("-i", "--input", type=Path, default=DEFAULT_INPUT, help="HTML base modular")
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT, help="HTML single-file de saída")
    parser.add_argument("--css", type=Path, default=DEFAULT_CSS, help="Arquivo CSS (style.css)")
    parser.add_argument("--js", type=Path, default=DEFAULT_JS, help="Arquivo JS (app.js)")
    parser.add_argument(
        "--no-inline-assets",
        action="store_true",
        help="Não converter url(...) locais do CSS para Base64",
    )
    parser.add_argument(
        "--no-minify",
        action="store_true",
        help="Não minificar CSS e HTML",
    )
    args = parser.parse_args()

    build_single_file(
        input_html=args.input,
        output_html=args.output,
        css_path=args.css,
        js_path=args.js,
        inline_assets=not args.no_inline_assets,
        minify=not args.no_minify,
    )


if __name__ == "__main__":
    main()
