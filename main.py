# Pontifícia Universidade Católica do Paraná
# Disciplina: Raciocínio Computacional
# Aluno: Enzo Jeremias Mantelli Rossetto
# Atividade Somativa 1: Protótipo inicial

# Importação do método para:
# pegar um valor randomico dentro de uma string,
# gerar lista randomizada a partir de outra e
# embaralhar uma lista
from random import choice, sample, shuffle

# Importação do namedtuple para criar dados identificados
from collections import namedtuple

# Definição de uma tupla para a base da estrutura dos dados
Dado = namedtuple('Dado', ['cor', 'faces'])


def lancar_dado(dado_lancado):
    """
        Retorna um lado de forma aleatória do Dado recebido.

        :param dado_lancado: Estrutura Dado que será usada para obter uma face em aleatório.
        :return: "C" or "T" or "P"
    """
    return choice(dado_lancado.faces)


def gerar_tubo_embaralhado():
    """
        Gera um tubo com 13 dados embaralhados sendo 6 verdes, 4 amarelos e 3 vermelhos
        :return: List[Dado]
    """

    tubo = []

    # Definição dos tipos de dados
    # Significados das letras: C = cérebro, T = tiro e P = passos
    dado_verde = Dado(cor='verde', faces=("C", "P", "C", "T", "P", "C"))
    dado_amarelo = Dado(cor='amarelo', faces=("T", "P", "C", "T", "P", "C"))
    dado_vermelho = Dado(cor='vermelho', faces=("T", "P", "T", "C", "P", "T"))

    # Adicionar os dados verdes ao tubo
    for _ in range(6):
        tubo.append(dado_verde)

    # Adicionar os dados amarelos ao tubo
    for _ in range(4):
        tubo.append(dado_amarelo)

    # Adicionar os dados vermelhos ao tubo
    for _ in range(3):
        tubo.append(dado_vermelho)

    # Gera um tubo com dados embaralhados
    return sample(tubo, len(tubo))


def cadastrar_jogadore():
    """
        Realiza o cadastro dos jogadores retornando uma estrutura em dicioário como a seguinte:
        :return: { "nome_jogador": {"tiros": 0, "cerebros": 0, "passos": 0}, ... }
    """

    # Mensagem para conseguir a quantia de jogadores
    numero_jogadores = int(input("Informe o número de jogadores: "))

    while numero_jogadores < 2:
        # Adverte o jogador e pede um novo valor
        print("\nZombie Dice deve ser jogado por pelo menos duas pessoas!")
        numero_jogadores = int(input("Informe o número de jogadores: "))

    # Lista com o nome dos jogadores
    lista_jogadores = {}

    # Pula uma linha para melhorar a leitura
    print("")

    # Recebe os nomes dos jogadores
    for i in range(0, numero_jogadores):
        novo_jogador = input(f"Digite no nome do jogador {i + 1}: ")

        while novo_jogador in lista_jogadores:
            print(f"Jogador {novo_jogador} já incluso anteriormente")
            novo_jogador = input(f"Digite um nome diferente de {novo_jogador} para o jogador {i + 1}: ")

        # Inicializa o score do jogador
        lista_jogadores[novo_jogador] = {"tiros": 0, "cerebros": 0, "passos": 0}

    # returna os jogadores cadastrados
    return lista_jogadores


def dados_no_copo(dados_tubo):
    """
    Recebe os dados restantes no tubo e retorna os três dados selecionados para serem rolados

    :param dados_tubo: Dados presentes no tubo
    :return: List[Dado]
    """

    dados_copo = []

    # Retira os 3 primeiros dados do tubo
    for _ in range(3):
        dados_copo.append(dados_tubo.pop(0))

    print(f"Dados no copo: {dados_copo[0].cor}, {dados_copo[1].cor}, {dados_copo[2].cor}\n")

    return dados_copo


def lancar_dados_copo(jogador_turno, dados_copo, dados_tubo):
    """
        Lança os três dados no existentes no copo, altera o score do jogador e retorna para o tubo
        os dados que tiveram valor 'passos'

        :param jogador_turno: jogador atual
        :param dados_copo: três dados existentes no copo
        :param dados_tubo: dados restantes no copo
    """

    # Joga os dados para conseguir seus valores
    for dado in dados_copo:
        valor_dado = lancar_dado(dado)

        if valor_dado == "C":
            print(f"Dado {dado.cor} - Você capturou o humano e comeu um CÉREBRO!")
            jogador_turno["cerebros"] += 1
        elif valor_dado == "T":
            print(f"Dado {dado.cor} - O humano ATIROU em você! Cuidado para não morrer.")
            jogador_turno["tiros"] += 1
        else:
            print(f"Dado {dado.cor} - Os PASSOS do humano foram mais rápidos e ele fugiu! Vá atrás dele outra vez.")
            jogador_turno["passos"] += 1
            dados_tubo.append(dado)  # Devolve o dado para o tubo
            shuffle(dados_tubo)  # Embaralha o tubo outra vez


def score_jogador(lista_jogadores, jogador_turno):
    """
        Mostra a pontuação atual do jogador recebido

        :param lista_jogadores: dicionário com os jogadores
        :param jogador_turno:  nome do jogador atual
    """

    print(f"\nA potuação de {jogador_turno} até agora é:")
    print(f"Cérebros comidos: {lista_jogadores[jogador_turno]['cerebros']}")
    print(f"Tiros recebidos: {lista_jogadores[jogador_turno]['tiros']}")
    print(f"Humanos que fugiram: {lista_jogadores[jogador_turno]['passos']}\n")


def zombie_dice():
    """
        Executa o jogo Zombie Dice
    """

    # Cadastra os jogadores dessa partida
    jogadores = cadastrar_jogadore()
    quantia_jogadores = len(jogadores)

    # Controle do loop de jogo
    vencedor = ''
    contagem_derrotados = 0

    while vencedor == '' and contagem_derrotados < quantia_jogadores - 1:
        # Executa os turnos dos jogadores
        for jogador in jogadores:

            # Caso haja vencedor, o jogo passa todos os turnos restantes e encerra
            if vencedor != '':
                continue

            continuar_turno = "s"  # controla se continua o turno por escolha
            tubo_dados = gerar_tubo_embaralhado()  # inicia um novo tubo de dados

            # Condições que permitem o jogador a continuar o turno ou não
            vitoria = jogadores[jogador]["cerebros"] >= 13
            derrota = jogadores[jogador]["tiros"] >= 3
            dados_suficientes_continuar = len(tubo_dados) >= 3

            # Caso seja uma nova rodada, passa o turno do jogador que perdeu em rodada anterior
            if derrota:
                print(f"\n{jogador} já foi derrotado. Passando turno para o próximo.\n")
                continue

            # Validação se é possível continuar o turno
            turno_possivel = not vitoria and not derrota and dados_suficientes_continuar

            print(f"{jogador} é o zumbi da vez!")
            print("Capture os humanos e coma seus cérebros!")

            # Jogador continua enquanto desejar ou for possível
            while continuar_turno.lower() == "s" and turno_possivel:
                # Pula uma linha para melhorar separação das mensagens
                print()

                # Armazena os dados desta jogada
                dados_turno = dados_no_copo(tubo_dados)
                lancar_dados_copo(jogadores[jogador], dados_turno, tubo_dados)

                # Reavalia condições de vitória ou derrota
                vitoria = jogadores[jogador]["cerebros"] >= 13
                derrota = jogadores[jogador]["tiros"] >= 3

                # Valida condições para encerrar ou continuar o jogo
                if vitoria:
                    print(f"\nVocê VENCEU! Os humanos nunca serão páreos para os zumbis!")
                    vencedor = jogador
                    break
                elif derrota:
                    print("\nVocê PERDEU! Os cérebros dos humanos foram mais astutos dessa vez.")
                    contagem_derrotados += 1
                    break
                else:
                    score_jogador(jogadores, jogador)

                    print("Quer continuar caçando humanos?")
                    continuar_turno = input("Digite S para sim ou N para não: ")
                    dados_suficientes_continuar = len(tubo_dados) >= 3

                    # Garante uma resposta válida
                    while continuar_turno.lower() != "s" and continuar_turno.lower() != "n":
                        print("\nResposta inválida!")
                        continuar_turno = input("Digite S para sim ou N para não: ")

                    # Se for necessário, gera um novo tubo para continuar jogando
                    if continuar_turno.lower() != "s" and not dados_suficientes_continuar:
                        tubo_dados = gerar_tubo_embaralhado()
                    elif continuar_turno.lower() == "n":
                        jogadores[jogador]["tiros"] = 0
                        jogadores[jogador]["passos"] = 0

    # Caso não haja vencedor por capturar 13 cérebros encontra o último sobrevivente
    if vencedor == '':
        for jogador in jogadores:
            if jogadores[jogador]['tiros'] < 3:
                vencedor = jogador

    print(f"\n{vencedor} foi o zumbi vencedor desta partida!\n")

    # Verifica se desejam jogar outra vez
    print("Quer caçar cérebros outra vez?")
    jogar_novamente = input("Digite S para sim ou N para não: ")

    # Garante uma resposta válida
    while jogar_novamente.lower() != "s" and jogar_novamente.lower() != "n":
        print("\nResposta inválida!")
        jogar_novamente = input("Digite S para sim ou N para não: ")

    if jogar_novamente.lower() == "n":
        print("\nObrigado por jogar Zombie Dice!\n")
    else:
        print("\nE que uma nova caçada comece!\n")
        zombie_dice()


zombie_dice()
