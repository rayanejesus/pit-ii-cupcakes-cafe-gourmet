# Roteiro do vídeo final — Grão & Doçura v2.0

## 1. Abertura

Apresentar o objetivo do PIT-II, a identidade Grão & Doçura e a separação
entre frontend React/Vite, backend FastAPI e PostgreSQL em produção.

## 2. Catálogo

1. Abrir a loja em desktop.
2. Mostrar cupcakes e cafés com imagens distintas.
3. Pesquisar um produto inexistente e mostrar o estado vazio.
4. Remover a busca e filtrar por categoria.
5. Reduzir a janela para demonstrar a responsividade.

## 3. Carrinho e revisão

1. Adicionar dois produtos diferentes.
2. Aumentar a quantidade de um produto.
3. Diminuir a quantidade.
4. Remover um item.
5. Abrir o carrinho e mostrar subtotal, taxa de entrega de R$ 8,50 e total.
6. Preencher nome, e-mail, endereço e pagamento simulado.
7. Mostrar a etapa de revisão antes do envio.

## 4. Confirmação

1. Confirmar o pedido uma única vez.
2. Mostrar o número do pedido, itens, total e status inicial.
3. Explicar que Pix/cartão são apenas demonstração.
4. Não exibir credenciais ou valores secretos.

## 5. Evidências técnicas

Mostrar, sem expor segredos:

- Testes automatizados aprovados.
- Build de produção aprovado.
- Cálculo final feito no backend.
- Idempotência por `Idempotency-Key` e hash SHA-256.
- Migração PostgreSQL preparada, mas não executada durante a gravação.

## 6. Encerramento

Informar as pendências manuais: configurar variáveis da Vercel, aplicar a
migração revisada no Supabase e validar o domínio público sem proteção de SSO
bloqueando o preflight.
