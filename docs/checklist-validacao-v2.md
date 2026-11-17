# Checklist de validação — v2.0

## Preparação

- [ ] Confirmar branch `feat/pit-ii-v2`.
- [ ] Confirmar tag `v1.0-avaliacao` sem alterações.
- [ ] Usar banco local somente para testes isolados.
- [ ] Em produção, configurar PostgreSQL por `DATABASE_URL`.
- [ ] Não executar a suíte que usa `drop_all` contra Supabase.

## Catálogo

- [ ] Abrir o catálogo.
- [ ] Confirmar imagens distintas para cupcakes e cafés.
- [ ] Pesquisar um produto existente.
- [ ] Pesquisar um termo sem resultados.
- [ ] Confirmar mensagem de estado vazio.
- [ ] Filtrar por categoria.
- [ ] Verificar layout em celular e desktop.

## Carrinho e checkout

- [ ] Adicionar um produto.
- [ ] Adicionar um segundo produto.
- [ ] Aumentar quantidade.
- [ ] Diminuir quantidade.
- [ ] Remover item.
- [ ] Confirmar subtotal.
- [ ] Confirmar taxa fixa de R$ 8,50.
- [ ] Confirmar total igual a subtotal + frete.
- [ ] Validar nome obrigatório.
- [ ] Validar formato do e-mail.
- [ ] Validar endereço obrigatório.
- [ ] Selecionar Pix simulado ou cartão simulado.
- [ ] Revisar itens, endereço e valores antes da confirmação.
- [ ] Confirmar pedido.
- [ ] Conferir número, itens, total e status inicial.
- [ ] Tentar clique repetido e confirmar que não duplica o pedido.

## Backend

- [ ] Confirmar cálculo de preços pelo banco, sem valores monetários do cliente.
- [ ] Confirmar estoque insuficiente retorna erro claro.
- [ ] Confirmar mesma chave e mesmo payload retornam o pedido original.
- [ ] Confirmar mesma chave e payload diferente retornam `409`.
- [ ] Confirmar restrição única no PostgreSQL.
- [ ] Aplicar somente a migração incremental revisada.

## Comandos

```powershell
cd backend
..\.venv\Scripts\python.exe -m pytest -q

cd ..\frontend
npm test -- --run
npm run build
```

## Registro de execução

- Data:
- Responsável:
- Backend:
- Frontend:
- Build:
- Ambiente PostgreSQL:
- Observações:
