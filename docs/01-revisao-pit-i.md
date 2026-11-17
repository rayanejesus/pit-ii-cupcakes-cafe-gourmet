# 1. Revisão do PIT-I

## Contextualização

O projeto propõe uma loja virtual para comercialização de cupcakes artesanais, cafés gourmet e acompanhamentos por delivery. A revisão preserva as histórias de usuário do PIT-I e amplia a solução com persistência, operação administrativa e rastreamento.

## Problema e objetivos

O problema de negócio é a ausência de um canal digital simples para consulta de produtos, compra e acompanhamento da entrega. O objetivo geral é disponibilizar uma experiência de compra acessível e confiável. Objetivos específicos: organizar o catálogo, persistir pedidos, recalcular preços no servidor, controlar estoque e simular o fluxo operacional.

## Público e escopo

O público inclui clientes, administradores e entregadores. O escopo implementado nesta primeira entrega inclui catálogo, busca, categorias, carrinho persistido no navegador, checkout, pagamento simulado, pedidos e transições operacionais na API. Autenticação real, upload de imagens e integração financeira ficam fora do escopo atual.

## Rastreabilidade

US01 navegar catálogo → `GET /api/products` → tela inicial.
US02 filtrar produtos → parâmetros `search` e `category_id` → busca e categorias.
US04 adicionar ao carrinho → estado local e `localStorage` → botão Adicionar.
US05 editar carrinho → remoção e quantidade → modal de checkout.
US07 selecionar pagamento → `payment_method` PIX/CARTAO → checkout.
US08 rastrear pedido → status persistido → endpoints de pedido.
US10 consultar histórico → `GET /api/orders?email=` → API preparada para a tela de histórico.
US11–US15 → endpoints administrativos e de operação previstos na arquitetura.
