# Estratégia de acesso ao Supabase

Esta estratégia não foi aplicada. O SQL abaixo deve ser revisado e aprovado
antes de qualquer alteração no projeto Supabase.

## Arquitetura

- O navegador acessa somente a API FastAPI.
- O navegador não recebe `DATABASE_URL`, senha, `service_role` ou outra
  credencial PostgreSQL.
- A API usa a URL do Transaction Pooler em variável de ambiente.
- Os papéis `anon` e `authenticated` não precisam de acesso direto às tabelas
  quando o Supabase é usado apenas como banco do backend.
- A conexão do backend deve usar um papel dedicado com privilégios mínimos,
  preferencialmente criado pelo administrador do banco.

## SQL proposto para revisão

O exemplo restringe o acesso direto via PostgREST aos papéis públicos. Ele não
deve ser executado sem confirmar o projeto, o schema e o papel efetivamente
usado pelo backend.

```sql
-- Revisar antes de executar. Não usar em uma sessão de aplicação sem aprovação.
REVOKE ALL ON TABLE public.categories, public.products,
  public.orders, public.order_items
  FROM anon, authenticated;

REVOKE ALL ON SEQUENCE public.categories_id_seq, public.products_id_seq,
  public.orders_id_seq, public.order_items_id_seq
  FROM anon, authenticated;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
  REVOKE ALL ON TABLES FROM anon, authenticated;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
  REVOKE ALL ON SEQUENCES FROM anon, authenticated;
```

O backend deve receber apenas os privilégios necessários para executar as
operações da aplicação. O papel de conexão não deve ser exposto ao frontend.
Se futuramente o acesso direto pelo Supabase Auth/PostgREST for necessário,
deve-se modelar RLS por operação e por usuário antes de conceder `SELECT`,
`INSERT`, `UPDATE` ou `DELETE`.

## Verificações antes do deploy

1. Confirmar quais papéis são usados pelo backend.
2. Consultar privilégios atuais sem modificá-los.
3. Confirmar que `anon` e `authenticated` não possuem acesso direto
   desnecessário.
4. Confirmar que a API é o único caminho do frontend até o banco.
5. Aplicar RLS somente após definir as colunas de identidade e as políticas.

Consultas somente de leitura para a revisão:

```sql
SELECT grantee, table_name, privilege_type
FROM information_schema.role_table_grants
WHERE table_schema = 'public'
  AND table_name IN ('categories', 'products', 'orders', 'order_items')
ORDER BY grantee, table_name, privilege_type;

SELECT schemaname, tablename, policyname, roles, cmd, qual, with_check
FROM pg_policies
WHERE schemaname = 'public'
  AND tablename IN ('categories', 'products', 'orders', 'order_items');
```
