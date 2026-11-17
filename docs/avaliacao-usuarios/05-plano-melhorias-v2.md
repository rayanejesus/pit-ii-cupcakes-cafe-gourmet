# Plano de melhorias — versão 2.0

Este plano não implementa as melhorias. A priorização deverá ser revisada após a consolidação dos cinco formulários.

| Prioridade | Entrega planejada | Relação com QA | Critério de aceite futuro |
|---|---|---|---|
| Alta | Criar histórico e acompanhamento do pedido | QA-02, QA-04 | Cliente consulta pedidos por e-mail/sessão e visualiza a linha de status |
| Alta | Implementar autenticação, perfis e autorização | QA-01, QA-05 | Cliente, administrador e entregador acessam somente suas operações |
| Alta | Criar painel administrativo | QA-01 | Produtos, estoque e status de pedidos podem ser gerenciados pela interface |
| Média | Adicionar controles de quantidade no carrinho | QA-03 | Incremento, decremento e remoção atualizam subtotal corretamente |
| Média | Criar tela de detalhe e personalização | QA-06 | Ingredientes, alergênicos e opções permitidas são exibidos e enviados no pedido |
| Média | Criar interface de entregador | QA-02 | Entregador visualiza entregas atribuídas e atualiza etapas autorizadas |
| Média | Automatizar jornada com Playwright | Plano de testes | Compra completa executada em navegador em ambiente controlado |
| Baixa | Melhorar imagens e acessibilidade visual | Feedback dos usuários | Contraste, textos alternativos e navegação por teclado verificados |

## Gate antes da implementação

1. Preencher os cinco formulários.
2. Consolidar problemas recorrentes e sugestões.
3. Confirmar prioridade com o responsável pelo projeto.
4. Criar casos de teste para cada melhoria.
5. Só então iniciar a implementação da versão 2.0.
