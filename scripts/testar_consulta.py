from src.analytics.consultas import top_pontuadores

for nome, pontos in top_pontuadores():
    print(nome, pontos)