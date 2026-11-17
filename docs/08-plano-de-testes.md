# 8. Plano de testes

## Estratégia

Pytest/HTTPX validam API, persistência, estoque, preços e transições. Vitest/Testing Library validam renderização, busca e carrinho. Playwright está previsto para a jornada E2E quando o ambiente de navegador estiver disponível.

| ID | Caso | Resultado esperado | Resultado |
|---|---|---|---|
| CT01 | Consultar catálogo | 10 produtos demonstrativos | Executado |
| CT02 | Criar pedido | Total recalculado com frete de R$ 8,50 | Executado |
| CT03 | Exceder estoque | API responde 409 sem criar pedido | Executado |
| CT04 | Pagar pedido | Status muda para PAGO | Executado |
| CT05 | Buscar produto no front-end | Card é filtrado | Executado |
| CT06 | Adicionar ao carrinho | Contador é atualizado e estado persiste | Executado |
| CT07 | Jornada E2E em navegador | Não executado |
