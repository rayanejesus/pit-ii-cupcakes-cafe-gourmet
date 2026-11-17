# Avaliação acadêmica da versão 1.0

## Identificação da versão

- Projeto: Loja Virtual de Cupcakes e Cafés Gourmet
- Versão preservada: `v1.0-avaliacao`
- Commit avaliado: `2338950ee67071390e89ff39da0bcbb09ac3673a`
- Data da inspeção técnica: 17/11/2026
- Avaliações com usuários: ainda não realizadas

A tag foi criada antes da inclusão desta documentação para manter a versão avaliada imutável.

## Estado funcional verificado no código

| Área | Estado verificado | Evidência técnica |
|---|---|---|
| Catálogo | Implementado | `frontend/src/App.tsx`; `GET /api/products` |
| Busca por nome | Implementado | campo de busca e parâmetro `search` |
| Filtro por categoria | Implementado | botões de categoria e parâmetro `category_id` |
| Inclusão no carrinho | Implementado | função `add` e persistência em `localStorage` |
| Subtotal | Implementado | cálculo `subtotal` no componente React |
| Dados de entrega | Implementado | formulário de nome, e-mail e endereço |
| Pagamento simulado | Implementado | opções `PIX` e `CARTAO`; endpoint `/pay` |
| Criação do pedido | Implementado | `POST /api/orders`; total recalculado no servidor |
| Estoque | Implementado | validação e baixa no serviço de pedidos |
| Confirmação visual | Implementado | mensagem `Pedido #... criado!` |
| Histórico visual do cliente | Não identificado na interface atual | há endpoint `GET /api/orders?email=`, mas não há tela correspondente |
| Acompanhamento visual da entrega | Não identificado na interface atual | há status na API, mas não há tela de rastreamento |
| Painel administrativo | Não identificado na interface atual | há criação de produto na API, sem interface e sem autorização implementada |
| Interface de entregador | Não identificada | não há página ou componente específico |
| Autenticação e perfis | Não identificada | a versão atual não contém fluxo de login/autorização |
| Edição de quantidade no carrinho | Não identificada | a interface permite adicionar e remover, mas não possui controles de incremento/decremento |
| Detalhe e personalização de produto | Não identificada | o card mostra descrição, mas não há tela de detalhe ou opções de personalização |

## Testes automatizados executados

| Suíte | Comando | Resultado real |
|---|---|---|
| Backend | `python -m pytest -q` | 3 aprovados; 2 avisos de depreciação |
| Frontend | `npm test` | 2 aprovados |

Os avisos observados não impediram a execução: depreciação de `datetime.utcnow()` e aviso de compatibilidade do `TestClient` com a versão instalada de HTTPX.

As conclusões de “não identificada” acima são limitações observadas na implementação, não respostas ou avaliações dos cinco participantes.
