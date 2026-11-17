# Evolução para a versão 2.0

## Escopo da Etapa 0

Este documento registra o diagnóstico da versão 1.0, a referência preservada
para comparação e o plano de implementação. Nenhuma melhoria funcional da
versão 2.0 foi implementada nesta etapa.

## Referência da versão 1.0

- Branch de origem: `main`
- Referência identificável: tag `v1.0-avaliacao`
- Commit atual da base: `6744531`
- Branch de trabalho: `feat/pit-ii-v2`

A tag `v1.0-avaliacao` deve permanecer imutável. A validação inicial foi
executada antes da criação da branch:

- Backend: 11 testes aprovados.
- Frontend: 5 testes aprovados.
- Build de produção do Vite: aprovado.
- Avisos observados: depreciação do uso de `httpx` no `TestClient` do
  Starlette e de `datetime.utcnow()` no SQLAlchemy/modelo de pedidos.

## Diagnóstico técnico atual

### Frontend

- React, TypeScript, Vite e Tailwind.
- O estado do carrinho fica no `localStorage`; não há persistência server-side
  do carrinho.
- O catálogo permite pesquisa textual, filtro por categoria e inclusão no
  carrinho.
- O carrinho mostra somente o subtotal e remove um item inteiro; ainda não há
  controles de incremento/decremento.
- O checkout coleta nome, e-mail, endereço e método de pagamento simulado.
- A confirmação é exibida em uma mensagem após a criação do pedido, mas não
  há uma etapa separada de revisão nem bloqueio explícito contra cliques
  repetidos.
- O botão de confirmação exibe um valor calculado no cliente com frete fixo,
  enquanto o total definitivo é calculado pelo backend.
- Os produtos já possuem descrição, ingredientes, alergênicos e `image_url`
  no contrato, mas a interface atual não oferece uma tela de detalhes.
- O frontend chama a API por `VITE_API_URL`, normalizando o prefixo `/api`.

### Backend

- FastAPI com routers de catálogo (`/api/categories`, `/api/products`) e
  pedidos (`/api/orders`).
- SQLAlchemy possui os modelos `categories`, `products`, `orders` e
  `order_items`.
- A URL do banco é selecionada por `DATABASE_URL`; SQLite é somente o padrão
  local quando a variável não existe. PostgreSQL usa `psycopg` e SSL.
- `create_all` é incremental, mas a inicialização em ambiente serverless não
  deve ser usada como substituta de migrações controladas.
- O servidor calcula subtotal, frete e total a partir dos preços persistidos,
  sem confiar em preços enviados pelo navegador.
- A consulta e a gestão atuais de pedidos exigem
  `X-Order-Management-Token`, mas o checkout público retorna o pedido criado.
- Ainda não existe mecanismo de autorização por cliente para consultar ou
  cancelar o próprio pedido; o token atual é operacional e não representa
  identidade de cliente.
- O fluxo atual possui transições de status e pagamento simulado, mas não
  possui cancelamento público com validação de elegibilidade.

### Persistência e Vercel

- SQLite é adequado para desenvolvimento local, mas não oferece persistência
  confiável no filesystem efêmero de funções serverless.
- Produção deve continuar usando PostgreSQL persistente por `DATABASE_URL`.
- O seed deve ser executado explicitamente e nunca a cada requisição.
- Frontend e backend permanecem projetos Vercel separados; nenhuma alteração
  de deploy será executada nesta etapa.

## Dependências entre funcionalidades

1. **Valores do carrinho e checkout**
   - Primeiro definir um contrato único para subtotal, frete e total.
   - Depois implementar os controles de quantidade e a revisão.
   - A confirmação e a proteção contra duplicidade dependem da resposta
     idempotente do endpoint de criação de pedido.

2. **Detalhes de produto e imagens**
   - O modelo e o seed já possuem ingredientes, alergênicos e URLs.
   - A interface de detalhes pode ser implementada sem alteração do banco,
     desde que o catálogo continue retornando esses campos.
   - A troca de imagens deve preservar URLs licenciadas e validar carregamento
     no build/uso real.

3. **Consulta, histórico e cancelamento**
   - É necessário definir primeiro um mecanismo de identidade/autorização que
     não dependa de IDs sequenciais nem exponha dados de terceiros.
   - A consulta de status, o histórico e o cancelamento devem reutilizar esse
     mecanismo.
   - O backend deve validar as transições e a elegibilidade antes de qualquer
     alteração; o frontend somente refletirá o resultado.

4. **Entrega**
   - A previsão será apresentada como estimativa, com regra explícita e sem
     promessa de prazo real.
   - Ela depende do status do pedido e deve ser incluída no contrato de
     consulta antes da implementação visual.

## Plano de implementação após aprovação

### Fase A — Correções prioritárias

- Criar uma função compartilhada de valores monetários no frontend e alinhar
  o contrato de resposta do backend.
- Exibir subtotal, taxa de entrega e total na revisão e no checkout.
- Adicionar incremento, decremento e remoção de itens, respeitando estoque
  conhecido sem substituir a validação do servidor.
- Substituir imagens repetidas por recursos distintos com licença adequada.
- Separar a revisão da confirmação e mostrar número do pedido e mensagem de
  sucesso.
- Impedir submissões duplicadas durante uma requisição em andamento e definir
  uma estratégia server-side para repetição da mesma confirmação.

### Fase B — Melhorias funcionais

- Adicionar visualização de detalhes com ingredientes e alergênicos.
- Criar consulta autorizada de status.
- Criar histórico autorizado sem permitir acesso por ID sequencial isolado.
- Apresentar previsão de entrega explicitamente marcada como estimativa.
- Implementar cancelamento apenas para estados elegíveis, validado no backend.

### Fase C — Validação e documentação

- Atualizar testes unitários e de integração do backend.
- Atualizar testes de componentes e fluxo do frontend.
- Validar catálogo, pesquisa, filtro, valores, quantidades, criação, revisão,
  confirmação, consulta autorizada e cancelamento permitido/negado.
- Executar build de produção e verificar o comportamento em viewport móvel.
- Documentar variáveis de ambiente, limitações de autorização e evidências
  reais de execução.

## Evidências previstas

Para cada fase serão registrados:

- arquivos e endpoints alterados;
- comandos executados e resultados;
- casos aprovados e casos rejeitados;
- confirmação de que o total final veio do servidor;
- confirmação de que pedidos de terceiros não podem ser consultados ou
  cancelados;
- resultado dos testes automatizados e do build;
- pendências que não puderem ser validadas sem um ambiente PostgreSQL real.

## Limitações conhecidas

- A tag da versão 1.0 é uma referência de avaliação, não uma garantia de
  disponibilidade de dados de produção.
- O token de gestão existente não deve ser tratado como autenticação completa
  de clientes.
- A validação real de PostgreSQL/Supabase depende da variável de ambiente
  disponível no ambiente de execução e não será simulada.

## Entrega da Etapa 1

Implementado na branch `feat/pit-ii-v2`:

- Discriminação de subtotal, taxa de entrega e total no carrinho e na revisão.
- Controles de aumento, diminuição e remoção de itens.
- Etapa de revisão com produtos, quantidades, dados de entrega e pagamento
  simulado antes do envio.
- Botão de confirmação desabilitado durante o envio e estado de submissão
  protegido no frontend.
- Confirmação explícita com o identificador do pedido e total retornado pelo
  servidor.
- Chave `Idempotency-Key` obrigatória no endpoint de criação de pedido.
- Tabela persistente `order_requests` com restrição única, vinculada ao pedido,
  para que repetições da mesma requisição retornem o pedido original entre
  instâncias serverless.
- O backend continua recalculando preços, subtotal, frete e total a partir dos
  produtos persistidos; nenhum preço ou frete é aceito do navegador.

### Arquivos alterados na Etapa 1

- `backend/app/controllers/orders.py`
- `backend/app/models/orders.py`
- `backend/app/services/order_service.py`
- `backend/tests/test_api.py`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `frontend/src/services/api.ts`
- `frontend/src/types/catalog.ts`

### Evidências da Etapa 1

- Backend: 13 testes aprovados.
- Frontend: 2 arquivos de teste e 7 testes aprovados.
- Build de produção Vite: aprovado.
- `git diff --check`: aprovado.

Os testes de API usam banco SQLite local isolado e podem executar `drop_all`
somente nesse ambiente de teste. Isso não deve ser executado contra Supabase.

### Pendências e limitações da Etapa 1

- A tabela `order_requests` precisa ser criada no PostgreSQL de produção por
  `python init_db.py` antes de usar a nova criação de pedidos, sem executar
  operações destrutivas.
- A taxa de entrega exibida pelo frontend é a taxa fixa atualmente definida no
  backend (`8.50`); o total definitivo continua sendo o retornado pelo
  backend.
- Histórico, consulta de status, cancelamento e acompanhamento permanecem
  fora desta entrega.
- Não há pagamento real.
- A proteção contra duplicidade depende de o cliente reutilizar a mesma chave
  quando repetir uma requisição; o frontend faz isso durante a confirmação.

## Endurecimento da idempotência

Cada criação de pedido calcula um SHA-256 de uma representação canônica dos
dados relevantes do checkout: cliente, endereço, pagamento e itens
(`product_id` e `quantity`). Os itens são ordenados antes do cálculo para que
uma simples diferença de ordem não gere um pedido diferente.

- Mesma chave e mesmo payload: retorna o pedido original.
- Mesma chave e payload diferente: retorna `409 Conflict`.
- A restrição única da chave continua sendo aplicada pelo banco, e o tratamento
  de `IntegrityError` mantém o comportamento entre instâncias concorrentes.
- O hash não inclui preço, subtotal, frete ou total enviados pelo cliente; esses
  valores continuam sendo calculados exclusivamente no backend.

Foi preparada a migração revisável
`database/migrations/002_add_order_request_hash.sql`. Ela adiciona a coluna de
forma incremental e não altera dados nem executa `DROP`. A coluna permanece
nullable para permitir a existência de registros antigos criados antes do
hash. Registros legados sem hash não devem ser reutilizados sem uma decisão de
backfill; a aplicação não os aceita silenciosamente como equivalentes.

### Evidências do endurecimento

- Teste de mesma chave e mesmo payload retornando o mesmo identificador.
- Teste de mesma chave e payload diferente retornando `409`.
- Teste de chave obrigatória e tratamento de conflito preservado.
- A concorrência continua protegida pela restrição única persistida no
  PostgreSQL; não há estado de idempotência em memória da função serverless.

## Entrega acadêmica v2.0

### Etapas concluídas

- Etapa 1: carrinho, revisão, valores server-side e confirmação idempotente.
- Etapa 2: validação de dados, mensagens de carregamento/erro/sucesso e
  confirmação detalhada.
- Etapa 3: imagens distintas por produto, estado vazio de busca e ajustes de
  layout responsivo preservando a identidade visual.
- Etapa 4: PostgreSQL preservado, migração incremental revisável e nenhuma
  operação destrutiva executada.
- Etapa 5: testes automatizados, build de produção e checklist manual.
- Etapa 6: laudo de qualidade, roteiro do vídeo e documentação de validação.

### Evidências executadas nesta entrega

- Backend: 14 testes aprovados.
- Frontend: 2 arquivos de teste e 7 testes aprovados.
- Build de produção Vite: aprovado.
- `git diff --check`: aprovado.
- Teste de catálogo confirmou 10 URLs de imagem distintas.
- Testes de idempotência confirmaram repetição equivalente e conflito de
  payload divergente.

### Migrações e produção

- A coluna `order_requests.request_hash` deve ser criada pela migração
  `database/migrations/002_add_order_request_hash.sql`.
- A tabela `order_requests` deve existir antes de criar pedidos na versão
  endurecida; `backend/init_db.py` pode criar tabelas ausentes de forma
  incremental.
- Nenhuma migração foi executada no Supabase durante esta entrega.
- A conexão real com PostgreSQL precisa ser validada no ambiente de produção
  sem expor a URL ou credenciais.

### Pendências para publicação

- Configurar `DATABASE_URL`, `FRONTEND_ORIGINS` e
  `ORDER_MANAGEMENT_TOKEN` no projeto backend da Vercel.
- Configurar `VITE_API_URL` no projeto frontend da Vercel.
- Remover/configurar a proteção SSO da Vercel que possa redirecionar
  requisições `OPTIONS`.
- Aplicar a migração revisada no PostgreSQL e validar `SELECT 1`, tabelas e
  criação idempotente de pedido.
- Executar o checklist manual e preencher os resultados reais dos cinco
  participantes; nenhum resultado foi inventado neste documento.
