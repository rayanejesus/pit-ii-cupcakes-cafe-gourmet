# Laudo de qualidade — v2.0

## Escopo

Este laudo registra somente correções observadas e verificadas no código e nos
testes da versão 2.0. Não contém avaliações inventadas de usuários.

## Problemas observados e correções

| ID | Problema observado | Correção realizada | Evidência |
|---|---|---|---|
| V2-01 | O carrinho não permitia ajustar a quantidade individualmente. | Controles de aumentar, diminuir e remover item. | Testes de interação do frontend. |
| V2-02 | O checkout não discriminava frete e total em uma etapa de revisão. | Resumo com subtotal, taxa fixa de R$ 8,50 e total antes da confirmação. | Testes de frontend e cálculo server-side. |
| V2-03 | Cliques repetidos poderiam enviar a confirmação mais de uma vez. | Botão desabilitado durante o envio e `Idempotency-Key` persistida no banco. | Testes de repetição e conflito de chave. |
| V2-04 | A mesma URL de imagem era usada para todos os produtos. | URLs distintas para cupcakes e cafés no seed idempotente. | Inspeção do seed e teste/build locais. |
| V2-05 | Busca sem resultado não apresentava orientação. | Estado vazio com mensagem e sugestão de remover filtros. | Teste de componente previsto no checklist. |
| V2-06 | A confirmação não detalhava itens e status inicial. | Confirmação com número, itens, total e status inicial. | Teste de confirmação do frontend. |

## Validação automatizada

- Backend: preencher com o resultado do comando executado na entrega.
- Frontend: preencher com o resultado do comando executado na entrega.
- Build: preencher com o resultado do comando executado na entrega.
- PostgreSQL: validar somente após aplicar as migrações revisadas no ambiente
  apropriado; não usar SQLite para declarar a conexão de produção.

## Avaliação dos cinco participantes

Os campos abaixo devem ser preenchidos somente após a execução real dos testes:

| Participante | Data | Funcionalidades testadas | Funcionaram | Problemas encontrados | Funcionalidades ausentes |
|---|---|---|---|---|---|
| Participante 1 |  |  |  |  |  |
| Participante 2 |  |  |  |  |  |
| Participante 3 |  |  |  |  |  |
| Participante 4 |  |  |  |  |  |
| Participante 5 |  |  |  |  |  |

## Limitações

- Pix e cartão continuam simulados.
- Não foram implementados autenticação completa, histórico, cancelamento ou
  acompanhamento avançado nesta entrega.
- A Vercel exige PostgreSQL persistente; SQLite serve apenas para execução
  local/testes isolados.
