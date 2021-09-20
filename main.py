# Pontifícia Universidade Católica do Paraná
# Disciplina: Raciocínio Computacional
# Aluno: Enzo Jeremias Mantelli Rossetto
# Atividade Somativa 1: Protótipo inicial

# Importação do método para:
# pegar um valor randomico dentro de uma string,
# gerar lista randomizada a partir de outra e
# embaralhar uma lista
from random import choice, sample, shuffle

# Definição dos tipos de dados
# Significados das letras: C = cérebro, T = tiro e P = passos

DADO_VERDE = ("C", "P", "C", "T", "P", "C")
DADO_AMARELO = ("T", "P", "C", "T", "P", "C")
DADO_VERMELHO = ("T", "P", "T", "C", "P", "T")


def rolar_dado(dado_rolado):
    return choice(dado_rolado)


def gerar_tubo_embaralhado():
    tubo = []

    # Adicionar os dados verdes ao tubo
    for _ in range(6):
        tubo.append(DADO_VERDE)

    # Adicionar os dados amarelos ao tubo
    for _ in range(4):
        tubo.append(DADO_AMARELO)

    # Adicionar os dados vermelhos ao tubo
    for _ in range(3):
        tubo.append(DADO_VERMELHO)

    # Gera um tubo com dados embaralhados
    return sample(tubo, len(tubo))


def cadastrar_jogadore():
    # Mensagem para conseguir a quantia de jogadores
    numero_jogadores = int(input("Informe o número de jogadores: "))

    while numero_jogadores < 2:
        # Adverte o jogador e pede um novo valor
        print("\nZombie Dice deve ser jogado por pelo menos duas pessoas!")
        numero_jogadores = int(input("Informe o número de jogadores: "))

    # Lista com o nome dos jogadores
    lista_jogadores = []

    # Pula uma linha para melhorar a leitura
    print("")

    # Recebe os nomes dos jogadores
    for i in range(0, numero_jogadores):
        novo_jogador = input(f"Digite no nome do jogador {i + 1}: ")
        lista_jogadores.append(novo_jogador)

    # returna os jogadores cadastrados
    return lista_jogadores


while True:
    # Cadastra os jogadores dessa partida
    jogadores = cadastrar_jogadore()

    # Contabiliza os pontos dos jogadores
    cerebros = [0] * len(jogadores)
    tiros = [0] * len(jogadores)

    # Executa os turnos dos jogadores
    for index_jogador in range(0, len(jogadores)):
        print(f"\n{jogadores[index_jogador]} é o zumbi da vez!")
        print("Capture os humanos e coma seus cérebros!")

        continuar_turno = "s"  # controla se continua o turno por escolha
        tubo_dados = gerar_tubo_embaralhado()  # inicia um novo tubo de dados

        # Condições que permitem o jogador a continuar o turno ou não
        vitoria = cerebros[index_jogador] >= 13
        derrota = tiros[index_jogador] >= 3
        dados_suficientes_continuar = len(tubo_dados) >= 3

        # Validação se é possível continuar o turno
        turno_possivel = not vitoria and not derrota and dados_suficientes_continuar

        # Jogador continua enquanto desejar ou for possível
        while continuar_turno.lower() == "s" and turno_possivel:
            # Pula uma linha para melhorar separação das mensagens
            print()

            # Armazena os dados desta jogada
            dados_turno = []

            # Retira os 3 primeiros dados do tubo
            for _ in range(3):
                dados_turno.append(tubo_dados.pop(0))

            # Joga os dados para conseguir seus valores
            for dado in dados_turno:
                valor_dado = rolar_dado(dado)

                if valor_dado == "C":
                    print("Você capturou o humano e comeu um CÉREBRO!")
                    cerebros[index_jogador] += 1
                elif valor_dado == "T":
                    print("O humano ATIROU em você! Cuidado para não morrer.")
                    tiros[index_jogador] += 1
                else:
                    print("Os PASSOS do humano foram mais rápidos e ele fugiu! Vá atrás dele outra vez.")
                    tubo_dados.append(dado)  # Devolve o dado para o tubo
                    shuffle(tubo_dados)  # Embaralha o tubo outra vez

            # Reavalia condições de vitória ou derrota
            vitoria = cerebros[index_jogador] >= 13
            derrota = tiros[index_jogador] >= 3

            # Valida condições para encerrar ou continuar o jogo
            if vitoria:
                print("\nVocê VENCEU! Os humanos nunca serão páreos para os zumbis!")
                vitoria = True
                break
            elif derrota:
                print("\nVocê PERDEU! Os cérebros dos humanos foram mais astutos dessa vez.")
                derrota = True
                break
            else:
                print(f"\nA potuação de {jogadores[index_jogador]} até agora é:")
                print(f"Cérebros comidos: {cerebros[index_jogador]}")
                print(f"Tiros recebidos: {tiros[index_jogador]}\n")

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
                    tiros[index_jogador] = 0

    # Verifica se desejam jogar outra vez
    print("\nQuer caçar cérebros outra vez?")
    jogar_novamente = input("Digite S para sim ou N para não: ")

    # Garante uma resposta válida
    while jogar_novamente.lower() != "s" and jogar_novamente.lower() != "n":
        print("\nResposta inválida!")
        jogar_novamente = input("Digite S para sim ou N para não: ")

    if jogar_novamente.lower() == "n":
        print("\nObrigado por jogar Zombie Dice!\n")
        break
    else:
        print("\nE que uma nova caçada comece!\n")
