# Instruções para execução local pelos avaliadores

Estas instruções usam Windows PowerShell e não exigem Docker ou serviços pagos.

## Pré-requisitos

- Python 3.11 ou superior compatível com as dependências do projeto.
- Node.js e npm.
- Git.

## Preparar o projeto

```powershell
git clone https://github.com/rayanejesus/pit-ii-cupcakes-cafe-gourmet.git
cd pit-ii-cupcakes-cafe-gourmet
git checkout v1.0-avaliacao
```

Usar a tag garante que a avaliação ocorra na versão preservada, sem mudanças posteriores.

## Iniciar a API

Em um terminal:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python seed.py
python -m uvicorn app.main:app --reload
```

Mantenha esse terminal aberto. A API estará em `http://localhost:8000` e a documentação interativa em `http://localhost:8000/docs`.

## Iniciar o frontend

Em outro terminal:

```powershell
cd frontend
npm install
npm run dev
```

Abra o endereço mostrado pelo Vite, normalmente `http://localhost:5173`.

## Preparar a sessão de avaliação

1. Abra uma janela anônima.
2. Confirme que a página carrega produtos.
3. Use apenas nomes, e-mails e endereços fictícios.
4. Não use dados reais de cartão; o pagamento é simulado.
5. Execute [`01-roteiro-testes-manuais.md`](./01-roteiro-testes-manuais.md).
6. Preencha somente o formulário do participante correspondente.
7. Preserve mensagens de erro e evidências, sem alterar o código.

## Encerrar

Feche os dois processos com `Ctrl+C`. Os dados locais ficam em `cupcakes.db`, que não deve ser enviado ao Git.
