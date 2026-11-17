# Opções de hospedagem gratuita — análise sem deploy

Nenhum serviço foi criado ou configurado. Esta é somente uma análise técnica para decisão posterior.

## Alternativas

### Render

O Render documenta implantação de FastAPI como Web Service Python com comando de instalação e inicialização `uvicorn`. É a alternativa mais direta para a API. A versão atual usa SQLite em arquivo local; portanto, antes de hospedar seria necessário avaliar a persistência do disco e, para uso contínuo, migrar para banco gerenciado. O serviço gratuito pode dormir quando não utilizado, o que é aceitável para demonstração, mas deve ser informado aos avaliadores.

Fonte: [Render — Deploy a FastAPI App](https://render.com/docs/deploy-fastapi)

### GitHub Pages

O GitHub Pages hospeda arquivos estáticos e pode ser compatível com o build Vite do frontend. Ele não executa FastAPI nem oferece SQLite persistente. Só seria adequado para uma versão estática ou se a API fosse hospedada separadamente e o frontend recebesse uma URL pública configurada.

Fonte: [GitHub Docs — What is GitHub Pages?](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

## Recomendação para decisão

Para uma demonstração acadêmica integrada, avaliar primeiro um Web Service Python compatível com FastAPI e uma estratégia de banco persistente. Não fazer deploy da versão 1.0 sem:

1. autorização do responsável;
2. definição de onde o SQLite será persistido ou migração para PostgreSQL;
3. configuração de CORS para o domínio do frontend;
4. proteção de dados e credenciais;
5. teste da URL pública;
6. confirmação de que o plano gratuito vigente atende aos limites.

Até essa autorização, a avaliação deve ser executada localmente.
