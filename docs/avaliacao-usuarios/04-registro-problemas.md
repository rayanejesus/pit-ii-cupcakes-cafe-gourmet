# Registro inicial de problemas — QA

Os registros abaixo foram identificados por inspeção do código da versão 1.0. Eles não foram atribuídos a nenhum participante e não representam respostas dos formulários. Após os testes, acrescente evidências, frequência e impacto observados.

| ID | Problema técnico observado | Evidência na versão 1.0 | Impacto esperado | Status | Participante / evidência |
|---|---|---|---|---|---|
| QA-01 | Não foi identificada uma tela de administração de produtos, pedidos ou estoque | O frontend possui uma única experiência de loja; a criação administrativa existe somente na API | Administrador não consegue operar o sistema pela interface | Aberto para validação | |
| QA-02 | Não foi identificada uma tela de acompanhamento de entrega | A API possui status e transições, mas não há componente de rastreamento | Cliente não encontra visualmente as etapas do pedido | Aberto para validação | |
| QA-03 | O carrinho não apresenta controles para editar diretamente a quantidade | O componente permite adicionar novamente ou remover o item | Ajustar uma quantidade exige repetir a inclusão | Aberto para validação | |
| QA-04 | Não foi identificada uma tela de histórico de pedidos | Existe `GET /api/orders?email=`, mas não existe tela consumidora no frontend | Cliente não consulta facilmente pedidos anteriores | Aberto para validação | |
| QA-05 | Não foi identificado fluxo de autenticação e autorização por perfil | Não há login, sessão, middleware de autorização ou telas de perfil na versão | Operações administrativas não estão protegidas por usuário | Aberto para validação | |
| QA-06 | Não foi identificada tela de detalhe ou personalização de produto | Os cards exibem descrição, mas não há rota ou formulário de personalização | Cliente não personaliza cupcakes/cafés nem consulta uma página detalhada | Aberto para validação | |

“Aberto para validação” significa que o item será confrontado com a observação dos participantes; não significa que os participantes já o reportaram.
