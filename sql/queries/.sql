-- sql/queries/top_5_pontuadores.sql

SELECT dim_jogador.nome, SUM(fato_estatisticas_temporada.pontos) AS total_pontos
FROM fato_estatisticas_temporada
JOIN dim_jogador ON fato_estatisticas_temporada.player_id = dim_jogador.player_id
GROUP BY dim_jogador.nome
ORDER BY total_pontos DESC
LIMIT 5;