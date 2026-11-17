# Matriz de rastreabilidade da avaliação

Esta matriz relaciona requisitos e funcionalidades com o roteiro, os testes automatizados e a evidência que deverá ser coletada. A coluna “resultado da avaliação” permanece em branco até os testes com pessoas reais.

| Requisito / história | Funcionalidade implementada verificada | Teste manual | Teste automatizado | Evidência a coletar | Resultado da avaliação |
|---|---|---|---|---|---|
| US01 / catálogo | Cards de produtos | T01 | `test_health_and_catalog` | Captura ou anotação da listagem | |
| US02 / filtro | Busca e filtro de categoria | T02–T03 | Cobertura parcial pelo catálogo | Produto encontrado e categoria aplicada | |
| US04 / carrinho | Adição e persistência local | T04 | Teste React de adição | Contador e itens exibidos | |
| US05 / edição do carrinho | Remoção implementada; alteração direta de quantidade não identificada | T04–T05 | Não coberto | Ação tentada e resultado | |
| US07 / pagamento | PIX e cartão simulado | T07 | `test_order_recalculates_total_and_payment` | Opção selecionada | |
| US08 / rastreamento | Status existe na API; tela não identificada | T10 | Transição inválida coberta | Caminho encontrado pelo participante | |
| US10 / histórico | Endpoint por e-mail; tela não identificada | T10 | Não coberto | Busca realizada e resultado | |
| RF03 / dashboard administrativo | Não há interface identificada | T10 | Não coberto | Tela procurada | |
| RF05 / prescrição de catálogo/administração | API de criação de produto sem interface/autorização | T10 | Não coberto | Tela procurada | |
| RF14 / pedido e preço | Total recalculado no servidor | T05, T08–T09 | `test_order_recalculates_total_and_payment` | Subtotal, frete e total | |
| Integridade de estoque | Validação e baixa no serviço | T08 | `test_invalid_stock_and_transition` | Mensagem, se houver | |

