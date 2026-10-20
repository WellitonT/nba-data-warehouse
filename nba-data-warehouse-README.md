# NBA Data Warehouse

Pipeline ETL em Python que extrai estatísticas de temporada da API oficial da NBA, trata a qualidade dos dados e carrega em um warehouse SQLite com modelo dimensional. Projeto contínuo de portfólio em dados, evoluindo rumo a Machine Learning e MLOps.

## O que o projeto faz

```
nba_api → extract → transform → models → load → SQLite → analytics → dashboard
```

| Camada | Arquivo | Responsabilidade |
|---|---|---|
| extract | `src/extract/nba_api_client.py` | Busca dados da API com retry, backoff e logging estruturado |
| transform | `src/transform/limpeza.py` | Remove linhas `TOT` e corrige tipos numéricos |
| models | `src/models/estatistica_temporada.py` | `@dataclass` do domínio + factory function |
| load | `src/load/database.py` | Carga no SQLite, idempotente |
| analytics | `src/analytics/consultas.py` | Consultas analíticas (rankings, totais por time) |

## Modelo de dados

Modelo dimensional simples, com grão de temporada por jogador e time:

- `fato_estatisticas_temporada`: pontos, rebotes, assistências, roubos, bloqueios, minutos, jogos e idade, com `UNIQUE (player_id, team_id, season_id)`
- `dim_jogador`: `player_id`, `nome`
- `dim_time`: `team_id`, `sigla`

A dimensão de jogador é uma dimensão simples (sem histórico). Evoluí-la para SCD Type 2 está no roadmap.

## Decisões técnicas

**Ingestão resiliente.** A API `stats.nba.com` é instável. A extração faz retry com backoff e isola falhas por jogador, sem derrubar o lote inteiro.

**Linhas de totalização.** Para jogadores trocados de time no meio da temporada, a API devolve uma linha extra com o total (`TEAM_ABBREVIATION == "TOT"`). Sem removê-la, qualquer soma fica silenciosamente duplicada. A transformação remove essas linhas antes de qualquer agregação.

**Carga idempotente.** A constraint `UNIQUE` combinada com `INSERT OR IGNORE` garante que reexecutar o pipeline não duplica registros.

**Consultas seguras.** Métricas escolhidas pela interface passam por uma lista fechada (`METRICAS_PERMITIDAS`), porque nome de coluna não pode ser parâmetro SQL e interpolação sem validação abre injeção de SQL. Há teste cobrindo isso.

## Como rodar

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m src.pipeline
python -m streamlit run src/dashboard/app.py
```

## Testes

```powershell
python -m pytest tests/ -v
```

Os testes usam mock da API (sem rede) e um banco SQLite temporário isolado por teste.

## Dashboard

```powershell
pip install -r requirements-dashboard.txt
python -m streamlit run src/dashboard/app.py
```

Mostra rankings por temporada e métrica, totais por time e o estado do warehouse (linhas por tabela). Toda consulta fica em `src/analytics/consultas.py`; o dashboard só chama funções e desenha.

## Stack

Python 3.13 · `nba_api` · pandas · requests · SQLite · pytest · Streamlit · Docker (Dockerfile inicial no repositório)

## Status

**Concluído:** pipeline de quatro camadas (extract, transform, models, load), carga idempotente em SQLite, consultas analíticas e testes automatizados.

**Em andamento:** dashboard analítico e containerização.

**Roadmap:** SCD Type 2 na dimensão de jogador, coluna de data de carga para observabilidade, orquestração, CI com GitHub Actions, deploy em cloud e uso como base para modelos de Machine Learning.

## Limitações conhecidas

- Grão de temporada: não há dados jogo a jogo.
- Sem coluna de data de carga: não dá para auditar quando cada registro entrou no banco.
- A API da NBA bloqueia IPs de datacenter com frequência, então o ETL roda localmente e não em ambiente cloud.

## Autor

Welliton ([LinkedIn](https://www.linkedin.com/in/welliton-tiene-336bb7207/)) · projeto de uma trilha autodidata em dados, rumo a MLOps.
