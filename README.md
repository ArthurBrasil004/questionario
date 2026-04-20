# 💎 Questionário SG

Formulário multi-etapa condicional para pesquisa de mercado de joias em Maceió.
Respostas são salvas automaticamente em Excel.

## Estrutura do projeto

```
questionario_sg/
├── app.py            # App principal (Streamlit)
├── questions.py      # Perguntas dos dois questionários
├── style.css         # Estilos visuais
├── requirements.txt  # Dependências Python
├── .gitignore
└── README.md
```

## Como rodar localmente

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/questionario-sg.git
cd questionario-sg

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Rode o app
streamlit run app.py
```

Acesse em: **http://localhost:8501**

## Deploy no Streamlit Cloud

1. Suba o projeto no GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Clique em **"New app"**
4. Selecione o repositório e o branch
5. Em **"Main file path"** coloque `app.py`
6. Clique em **Deploy**

## Excel de respostas

O arquivo `respostas.xlsx` é criado automaticamente na raiz do projeto a cada nova submissão.
Na tela final, há um botão para baixar todas as respostas.

> **Atenção:** O `respostas.xlsx` está no `.gitignore` para não versionar dados reais.
> No Streamlit Cloud, o arquivo é temporário — baixe regularmente pelo botão de download.
