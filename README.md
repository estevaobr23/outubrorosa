# Página de vendas — Kit Ação Outubro Rosa

Página única (`index.html`: HTML + CSS + JS vanilla), sem dependências de runtime.

## Rodar / publicar
```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # gera dist/ (sobe a pasta dist/ na Vercel, Netlify etc.)
```

## O que editar
Tudo fica no topo do `<script>` em `index.html`:

```js
const OFERTA = {
  preco: "R$ 29,90",            checkoutUrl: "https://pay.cakto.com.br/dq92erc",         // Plano Completo
  precoBasico: "R$ 22,90",      checkoutUrlBasico: "https://pay.cakto.com.br/u6776bb",   // Plano Básico
  precoDownsell: "R$ 25,90",    checkoutUrlDownsell: "https://pay.cakto.com.br/4w79fej", // modal ao escolher o básico
  garantiaDias: 15,
};
```
Cakto: produto `5a4dd1b5-6f18-4e64-ba06-521ce1d523d5` com as 3 ofertas acima.
O botão do plano básico abre o modal de downsell; ele NÃO aponta para a Cakto, porque o
pixel da UTMify captura cliques em links de checkout e redireciona antes do modal abrir.
Enquanto `checkoutUrl` não for uma URL `https://`, os botões rolam até a oferta.
As UTMs (`utm_*`, `sck`, `src`, `fbclid`) que chegam na página são repassadas para o checkout
e guardadas na sessão (sobrevivem a um recarregamento).

`LOCAIS` (mesmo bloco) controla os cards da seção "Onde usar".

## Imagens
- `public/images/cartas/cartinha-XX.webp`: geradas das cartinhas finais por
  `python scripts/gerar_imagens.py`. Rode de novo quando novas cartinhas ficarem prontas
  e atualize `TOTAL_CARTAS` no script da página.
- `public/images/og-image.jpg`: imagem de compartilhamento (placeholder gerado).
- Plaquinha, cartaz, arte da caixa, tags e guia são **mockups em CSS** (escalam sozinhos).
  Para trocar por foto real, substitua o `<div class="mk">…</div>` do item por
  `<img src="images/plaquinha.webp" …>`. Há um comentário com o nome do arquivo em cada item
  da seção "Tudo o que você recebe".
