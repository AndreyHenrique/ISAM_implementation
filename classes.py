class Registro:
    def __init__(self, chave, dado):
        self.chave = chave
        self.dado = dado

    # Para printar a classe facilmente
    def __repr__(self):
        return f"({self.chave}, {self.dado})"

class Pagina:
    def __init__(self, limite=2, eh_overflow=False):
        self.registros = []  # Lista de objetos Registro 
        self.proxima_overflow = None  # Ponteiro para página de overflow 
        self.limite = limite
        self.eh_overflow = eh_overflow

class ISAM:
    def __init__(self):
        # Configuração da Estrutura Inicial Estática 
        # Nível Folha (Dicionário para acesso rápido via ponteiro simbólico)
        self.folhas = {
            'A': Pagina(), 'B': Pagina(), 'C': Pagina(),
            'D': Pagina(), 'E': Pagina(), 'F': Pagina()
        }
        
        # Inserção dos registros iniciais conforme a tabela 
        self._carregar_inicial('A', [10, 15])
        self._carregar_inicial('B', [20, 27])
        self._carregar_inicial('C', [33, 37])
        self._carregar_inicial('D', [40, 46])
        self._carregar_inicial('E', [51, 55])
        self._carregar_inicial('F', [63, 97])

        # Métricas 
        self.total_removidos = 0

    def _carregar_inicial(self, id_folha, chaves):
        for c in chaves:
            self.folhas[id_folha].registros.append(Registro(c, f"R{c}"))

    def navegar_indice(self, chave):
        custo = 1 # Raiz
        # Nível Raiz (Chave 40)
        if chave < 40:
            custo += 1 # Nível intermediário 1 (Esquerdo)
            # Nível Intermediário 1 (20, 33)
            if chave < 20: 
                return 'A', custo + 1 # Aponta para Folha A
            elif chave < 33: 
                return 'B', custo + 1 # Aponta para Folha B
            else: 
                return 'C', custo + 1 # Aponta para Folha C
        else:
            custo += 1 # Nível intermediário 1 (Direito)
            # Nível Intermediário 1 (51, 63)
            if chave < 51: 
                return 'D', custo + 1 # Aponta para Folha D
            elif chave < 63: 
                return 'E', custo + 1 # Aponta para Folha E
            else: 
                return 'F', custo + 1 # Aponta para Folha F

    def inserir(self, chave, dado):
        id_folha, _ = self.navegar_indice(chave)
        pagina_atual = self.folhas[id_folha]
        
        # Busca se já existe ou espaço na primária/overflows existentes
        while True:
            if len(pagina_atual.registros) < pagina_atual.limite:
                pagina_atual.registros.append(Registro(chave, dado))
                pagina_atual.registros.sort(key=lambda x: x.chave)
                return
            if pagina_atual.proxima_overflow is None:
                # Cria nova página de overflow 
                pagina_atual.proxima_overflow = Pagina(eh_overflow=True)
            pagina_atual = pagina_atual.proxima_overflow

    def buscar_igualdade(self, chave):
        id_folha, custo_base = self.navegar_indice(chave)
        pagina_atual = self.folhas[id_folha]
        custo_paginas = 0
        
        while pagina_atual:
            custo_paginas += 1
            for reg in pagina_atual.registros:
                if reg.chave == chave:
                    return reg, custo_base + custo_paginas
            pagina_atual = pagina_atual.proxima_overflow
        return None, custo_base + custo_paginas

    def remover(self, chave):
        id_folha, _ = self.navegar_indice(chave)
        anterior = None
        atual = self.folhas[id_folha]
        
        while atual:
            for i, reg in enumerate(atual.registros):
                if reg.chave == chave:
                    atual.registros.pop(i)
                    self.total_removidos += 1
                    # Se overflow ficar vazio, desconecta
                    if atual.eh_overflow and not atual.registros:
                        anterior.proxima_overflow = atual.proxima_overflow
                    return True
            anterior = atual
            atual = atual.proxima_overflow
        return False

    def buscar_intervalo(self, inicio, fim):
        resultados = []
        custo_total = 0
        # Percorre todas as folhas para garantir o intervalo (simplificação do ISAM)
        for id_folha in ['A', 'B', 'C', 'D', 'E', 'F']:
            _, custo_idx = self.navegar_indice(0) # Simula custo de chegar na folha
            custo_total += custo_idx
            atual = self.folhas[id_folha]
            while atual:
                custo_total += 1
                for reg in atual.registros:
                    if inicio <= reg.chave <= fim:
                        resultados.append(reg)
                atual = atual.proxima_overflow
        return resultados, custo_total

    def exibir_metricas(self):
        overflows = 0
        total_cadeia = 0
        for folha in self.folhas.values():
            atual = folha.proxima_overflow
            while atual:
                overflows += 1
                total_cadeia += 1
                atual = atual.proxima_overflow
        
        print("\n--- MÉTRICAS ISAM ---")
        print(f"Páginas Folha Primárias: {len(self.folhas)}")
        print(f"Total de Páginas de Overflow: {overflows}")
        print(f"Registros Removidos: {self.total_removidos}")
        if overflows > 0:
            print(f"Tamanho Médio das Cadeias de Overflow: {total_cadeia/len(self.folhas):.2f}")
