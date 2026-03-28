
from classes import ISAM

meu_isam = ISAM()

# Inserções 
insercoes = [
    (18, "R18"), (22, "R22"), (27, "R27"), (35, "R35"), (41, "R41"),
    (44, "R44"), (63, "R63"), (67, "R67"), (83, "R83"), (86, "R86"),
    (121, "R121"), (145, "R145")
]
for c, d in insercoes:
    meu_isam.inserir(c, d)

# Remoções 
remocoes = [27, 44, 67, 83, 145]
for c in remocoes:
    meu_isam.remover(c)

# Buscas de Exemplo
res, custo = meu_isam.buscar_igualdade(35)
print(f"Busca(35): {res}, Custo: {custo} nós")

res_int, custo_int = meu_isam.buscar_intervalo(20, 50)
print(f"Busca Intervalo(20, 50): {len(res_int)} registros encontrados, Custo: {custo_int} nós")

meu_isam.exibir_metricas()