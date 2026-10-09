"""Gera as imagens otimizadas da página a partir das cartinhas finais.

Uso:  python scripts/gerar_imagens.py
Saída: public/images/cartas/cartinha-XX.webp  (540x720, para a página)
       public/images/og-image.jpg             (1200x630, compartilhamento)
Rode de novo sempre que novas cartinhas forem finalizadas no lote.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

PAGINA = Path(__file__).resolve().parents[1]
RAIZ = PAGINA.parent
FINAIS = RAIZ / "producao" / "lote-01" / "cartas-finais"
REFERENCIA = RAIZ / "IMAGEM REFERENCIA OUTUBRO ROSA" / "1.png"
SAIDA = PAGINA / "public" / "images"
CARTAS = SAIDA / "cartas"

LARGURA, ALTURA = 540, 720


def fontes_cartas() -> list[tuple[int, Path]]:
    itens = [(1, REFERENCIA)]
    for arq in sorted(FINAIS.glob("cartinha-*.png")):
        itens.append((int(arq.stem.split("-")[1]), arq))
    return itens


def converter_cartas() -> list[Path]:
    CARTAS.mkdir(parents=True, exist_ok=True)
    geradas = []
    for numero, origem in fontes_cartas():
        im = Image.open(origem).convert("RGB").resize((LARGURA, ALTURA), Image.LANCZOS)
        destino = CARTAS / f"cartinha-{numero:02d}.webp"
        im.save(destino, "WEBP", quality=80, method=6)
        geradas.append(destino)
    return geradas


def og_image(cartas: list[Path]) -> None:
    fundo = Image.new("RGB", (1200, 630), (253, 243, 245))
    escolhidas = [cartas[i] for i in (2, 6, 0, 17, 10) if i < len(cartas)]
    angulos = (-16, -8, 0, 8, 16)
    centro_x = 820
    for i, (arq, ang) in enumerate(zip(escolhidas, angulos)):
        carta = Image.open(arq).convert("RGBA").resize((300, 400), Image.LANCZOS)
        sombra = Image.new("RGBA", (340, 440), (0, 0, 0, 0))
        ImageDraw.Draw(sombra).rounded_rectangle((20, 26, 320, 426), 18, fill=(120, 40, 60, 60))
        sombra = sombra.filter(ImageFilter.GaussianBlur(12))
        sombra.alpha_composite(carta, (20, 20))
        girada = sombra.rotate(-ang, expand=True, resample=Image.BICUBIC)
        x = centro_x + (i - 2) * 70 - girada.width // 2
        y = 115 + abs(i - 2) * 14
        fundo.paste(girada, (x, y), girada)
    d = ImageDraw.Draw(fundo)
    serif = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 58)
    corpo = ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf", 28)
    d.text((70, 70), "KIT DIGITAL IMPRIMÍVEL", font=corpo, fill=(200, 50, 95))
    for n, linha in enumerate(("Kit Ação", "Outubro Rosa")):
        d.text((70, 130 + n * 70), linha, font=serif, fill=(120, 24, 52))
    for n, linha in enumerate(("100 cartinhas de força e", "acolhimento prontas para", "imprimir, recortar e montar.")):
        d.text((70, 310 + n * 42), linha, font=corpo, fill=(90, 50, 60))
    fundo.save(SAIDA / "og-image.jpg", "JPEG", quality=85, optimize=True)


if __name__ == "__main__":
    geradas = converter_cartas()
    og_image(geradas)
    print(f"{len(geradas)} cartinhas -> {CARTAS}")
