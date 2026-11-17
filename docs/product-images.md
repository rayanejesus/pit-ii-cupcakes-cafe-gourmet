# Imagens do catálogo

As imagens do catálogo são empacotadas em
`frontend/public/images/products/` e servidas pelo próprio frontend. O
frontend seleciona a imagem local pelo nome do produto, mantendo compatibilidade
com registros existentes no PostgreSQL que ainda contenham uma URL externa.

As fotografias foram obtidas do Unsplash, que permite uso comercial e não
comercial conforme a [Unsplash License](https://unsplash.com/license). Os
arquivos foram baixados com largura de 800 px e parâmetros de compressão
compatíveis com a interface.

| Produto | Arquivo local | Fonte |
|---|---|---|
| Red Velvet | `red-velvet.jpg` | [Unsplash](https://images.unsplash.com/photo-1576618148400-f54bed99fcfd) |
| Chocolate Trufado | `chocolate-trufado.jpg` | [Unsplash](https://images.unsplash.com/photo-1486427944299-d1955d23e34d) |
| Baunilha com Morango | `baunilha-morango.jpg` | [Unsplash](https://images.unsplash.com/photo-1587668178277-295251f900ce) |
| Cenoura com Brigadeiro | `cenoura-brigadeiro.jpg` | [Unsplash](https://images.unsplash.com/photo-1519869325930-281384150729) |
| Doce de Leite | `doce-leite.jpg` | [Unsplash](https://images.unsplash.com/photo-1558301211-0d8c8ddee6ec) |
| Limão Siciliano | `limao-siciliano.jpg` | [Unsplash](https://images.unsplash.com/photo-1603532648955-039310d9ed75) |
| Espresso Gourmet | `espresso-gourmet.jpg` | [Unsplash](https://images.unsplash.com/photo-1495474472287-4d71bcdd2085) |
| Cappuccino Cremoso | `cappuccino-cremoso.jpg` | [Unsplash](https://images.unsplash.com/photo-1509042239860-f550ce710b93) |
| Latte de Baunilha | `latte-baunilha.jpg` | [Unsplash](https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd) |
| Café Especial Coado | `cafe-especial-coado.jpg` | [Unsplash](https://images.unsplash.com/photo-1447933601403-0c6688de566e) |

Cada produto possui arquivo próprio. Se um arquivo falhar no navegador, a
interface usa `red-velvet.jpg` como fallback, sem depender de uma URL externa.
