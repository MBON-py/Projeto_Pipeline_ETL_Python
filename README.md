# Pipeline de Dados com Python, PostgreSQL e Power BI

Este projeto tem como objetivo criar uma pipeline de dados para processar, validar e armazenar dados de um arquivo CSV, preparando-os para consumo no Power BI. Utilizamos ferramentas como  **Pandas**,  **Pandas Profiling**,  **Pydantic**,  **Streamlit**  e  **PostgreSQL**  para garantir a qualidade e integridade dos dados.

----------

## Sumário

1.  Visão Geral do Projeto
    
2.  Ferramentas e Bibliotecas Utilizadas
    
3.  Etapas do Projeto
    
4.  Diagrama de Arquitetura
    
5.  Como Executar o Projeto
    
6.  Documentação das Bibliotecas
    
7.  Contribuição
    
8.  Licença
    

----------

## Visão Geral do Projeto

O projeto consiste em uma pipeline de dados que realiza as seguintes etapas:

1.  **Leitura e Análise Exploratória de Dados (EDA)**: Utilizamos o  **Pandas Profiling**  para identificar problemas como valores faltantes, outliers e inconsistências.
    
2.  **Validação de Dados**: Com o  **Pydantic**, definimos um esquema de validação para garantir a integridade dos dados. Uma aplicação interativa foi criada com  **Streamlit**  para facilitar a validação.
    
3.  **Limpeza e Transformação**: Os dados são limpos e transformados usando  **Pandas**, corrigindo problemas identificados na etapa de EDA.
    
4.  **Armazenamento no PostgreSQL**: Os dados processados são armazenados em um banco de dados  **PostgreSQL**  para persistência e consulta.
    
5.  **Consumo no Power BI**: O Power BI se conecta ao PostgreSQL para criar visualizações e dashboards.
    

----------

## Ferramentas e Bibliotecas Utilizadas

-   **Python**: Linguagem de programação principal.
    
-   **Pandas**: Manipulação e análise de dados.
    
-   **Pandas Profiling**: Geração de relatórios de análise exploratória.
    
-   **Pydantic**: Validação de dados baseada em esquemas.
    
-   **Streamlit**: Criação de uma aplicação web para validação interativa de dados.
    
-   **PostgreSQL**: Banco de dados relacional para armazenamento dos dados processados.
    
-   **Power BI**: Ferramenta de visualização e análise de dados.
    

----------

## Etapas do Projeto

1.  **Pré-Processamento**:
    
    -   Leitura do arquivo CSV com  **Pandas**.
        
    -   Análise exploratória com  **Pandas Profiling**.
        
    -   Validação interativa com  **Streamlit**.
        
2.  **ETL (Extração, Transformação e Carga)**:
    
    -   Definição do esquema de dados com  **Pydantic**.
        
    -   Limpeza e transformação dos dados com  **Pandas**.
        
    -   Carga dos dados processados no  **PostgreSQL**.
        
3.  **Consumo**:
    
    -   Conexão do  **Power BI**  ao PostgreSQL para visualização dos dados.
        

----------

## Diagrama de Arquitetura

Abaixo está o diagrama de arquitetura do projeto:

````mermaid 
---
config:
  theme: default
  look: classic
  layout: elk
---
flowchart TD
    A["📁 Arquivo CSV"] --> B["🔍 Análise Exploratória (Pandas Profiling)"]
    B --> C["✅ Validação de Dados (Streamlit + Pydantic)"]
    C --> D["🧹 Limpeza e Transformação (Pandas)"]
    D --> E["💾 Armazenamento no PostgreSQL"]
    E --> F["📊 Consumo no Power BI"]
    C -- 🚫 Erros de Validação --> G["📝 Relatório de Erros"]
    G --> A
````

----------

## Como Executar o Projeto

### Pré-requisitos

-   Python 3.8 ou superior.
    
-   PostgreSQL instalado e configurado.
    
-   Power BI Desktop (opcional, para visualização).
    

### Passos para Execução

1.  **Clone o repositório**:

````bash
    git clone https://github.com/seu-usuario/nome-do-repositorio.git
    cd nome-do-repositorio
````

2.  **Configure o ambiente virtual**:
```bash    
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
```    
3.  **Instale as dependências**:
```bash    
    pip install -r requirements.txt
```    
4.  **Execute a aplicação de validação com Streamlit**:
```bash    
    streamlit run app_validacao.py
```    
5.  **Conecte-se ao PostgreSQL**: *(SERÁ CONSTRUIDO EM BREVE)*
    
    -   Configure as credenciais do banco de dados no arquivo  `config.py`.
        
    -   Execute o script de carga no PostgreSQL:
    ````bash         
        python carregar_postgres.py
    ````    
6.  **Conecte o Power BI ao PostgreSQL**: 
    
    -   Use as credenciais do banco de dados para se conectar e criar visualizações.
        

----------

## Documentação das Bibliotecas

Aqui estão os links para a documentação das bibliotecas utilizadas:

-   [Pandas](https://pandas.pydata.org/docs/)
    
-   [Pandas Profiling](https://pandas-profiling.ydata.ai/docs/master/)
    
-   [Pydantic](https://docs.pydantic.dev/latest/)
    
-   [Streamlit](https://docs.streamlit.io/)
    
-   [PostgreSQL](https://www.postgresql.org/docs/)
    
-   [Power BI](https://learn.microsoft.com/en-us/power-bi/)
    

----------

## Contribuição

Contribuições são bem-vindas! Siga os passos abaixo:

1.  Faça um fork do repositório.
    
2.  Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
    
3.  Commit suas mudanças (`git commit -m 'Adicionando nova feature'`).
    
4.  Push para a branch (`git push origin feature/nova-feature`).
    
5.  Abra um Pull Request.
    

----------

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo  [LICENSE](https://license/)  para mais detalhes.


⭐️ From [Maria Benussy]([https://github.com/seu-username](https://github.com/MBON-py))