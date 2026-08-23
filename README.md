# NBA Data Warehouse

Data warehouse de estatísticas da NBA, construído como projeto contínuo de portfólio em Engenharia de Dados, evoluindo de ingestão simples até uma arquitetura completa de dados — com destino planejado até Machine Learning.

## Sobre o projeto

Diferente de um exercício isolado, este projeto acompanha a trilha de aprendizado inteira: começa com ingestão de dado real via API oficial da NBA, evolui para um modelo dimensional de data warehouse, e está planejado para, nas próximas fases, ganhar orquestração (Airflow), containerização (Docker) e evoluir para uma arquitetura de lakehouse — servindo depois como base de dados para modelos de Machine Learning.

## Por que NBA como domínio

Dataset escolhido após comparação com outras opções (F1, League of Legends, MotoGP), com base em três critérios: qualidade e maturidade da API disponível (`nba_api`), reconhecimento do domínio por recrutadores técnicos, e disponibilidade de dados de temporada ativa, permitindo trabalhar com dado que muda de verdade, não uma fotografia estática.

## Arquitetura

O projeto segue uma separação por camada de pipeline, inspirada em arquiteturas ETL/ELT reais:

```
nba-data-warehouse/
├── src/
│   ├── extract/
│   │   └── nba_api_client.py     # Busca dado bruto da API oficial da NBA
│   ├── transform/
│   │   └── limpeza.py             # Qualidade de dado: remoção de duplicatas, correção de tipos
│   ├── models/
│   │   └── estatistica_temporada.py  # Classes de domínio
│   ├── load/                      # Carga no banco de dados (em construção)
│   └── analytics/                 # Consultas e agregações (planejado)
├── sql/
│   ├── ddl/                       # Definição de schema (Star Schema)
│   └── queries/                   # Consultas analíticas
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── tests/
├── requirements.txt
└── pytest.ini
```

## Modelo de dados

Modelagem dimensional em **Star Schema**, escolhida por otimizar leitura analítica (menos joins, consultas mais simples e rápidas) em troca de alguma redundância de dado — trade-off padrão em data warehouses, que priorizam consulta sobre economia de espaço.

- **`fato_estatisticas_jogo`** — tabela fato central
- **`dim_jogador`** — modelada como **SCD Type 2**, preservando histórico de mudanças (ex.: trocas de time), em vez de sobrescrever o registro atual
- **`dim_time`**, **`dim_jogo`**, **`dim_temporada`** — dimensões de suporte

## Decisões técnicas de destaque

**Ingestão resiliente.** A API oficial da NBA (`stats.nba.com`) é conhecida por instabilidade de rede. A camada de extração implementa retry com backoff (até 3 tentativas por requisição, com espera entre elas) e timeout estendido, isolando falhas por jogador sem derrubar o processamento do lote inteiro.

**Tratamento de linhas de totalização.** A API devolve, para jogadores que trocam de time no meio da temporada, uma linha adicional com o total consolidado (`TEAM_ABBREVIATION == "TOT"`), junto às linhas individuais por time. Sem filtrar essa linha antes de agregações, qualquer soma de estatísticas fica silenciosamente duplicada. A camada de transformação detecta e remove essas linhas antes de qualquer cálculo.

**Correção de tipos.** A API devolve os dados com tipagem inconsistente internamente (colunas numéricas classificadas como `object` pelo pandas). A camada de transformação força a conversão explícita para tipos numéricos corretos, prevenindo bugs silenciosos em operações agregadas.

## Como rodar o projeto

```bash
git clone https://github.com/WellitonT/nba-data-warehouse.git
cd nba-data-warehouse

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

## Rodando os testes

```bash
python -m pytest tests/ -v
```

## Stack

- Python 3.13
- `nba_api` — cliente para a API oficial de estatísticas da NBA
- `pandas` — tratamento e transformação de dados
- `requests` — comunicação HTTP
- `pytest` — testes automatizados
- SQLite (planejado para a camada de carga)

## Status

**Concluído:** ingestão resiliente de estatísticas por temporada (com logging estruturado), tratamento de qualidade de dado (remoção de duplicatas, correção de tipos), modelagem inicial de domínio, testes automatizados para transformação e extração (com mock de chamadas de API, sem dependência de rede).

**Em construção:** camada de carga no banco de dados (SQLite), criação das tabelas do modelo dimensional.

**Planejado:** orquestração com Airflow, containerização com Docker, migração para armazenamento em cloud, evolução para arquitetura de lakehouse, e uso como base para modelos de Machine Learning.

## Autor

Welliton — projeto desenvolvido como parte de uma trilha autodidata em Engenharia de Dados, com trajetória planejada até Machine Learning e AI Engineering.