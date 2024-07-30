import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def clamp(n, min, max):
    if (n < min):
        return min
    elif (n > max):
        return max
    else:
        return n

from random import randint as rand

#informações sobre as dimensões da grade
gridInfo = {
    "width"     : 10,
    "height"    : 9,
    "barcos"    : 0
}

gridInfo["width"] = clamp(gridInfo["width"], 10, 26)
gridInfo["height"] = clamp(gridInfo["height"], 5, 9)

#array que será preenchida com dicionários, contendo a posição XxY do tile, se há algum barco no tile, e se ele já foi usado
grid = []

#array com as coordenadas do eixo X
coord = "abcdefghijklmnopqrstuvwxyz"

def criarGrade():
    #criar grade, da esquerda pra direita, de cima pra baixo
    global grid

    pos = {
        "x" : 0,
        "y" : 0,
    }

    for i in range(gridInfo["height"]):
        linha = []
        for j in range(gridInfo["width"]):
            x = pos["x"]
            y = pos["y"]
            pos["x"] += 1

            tile = {
                "x"     : x,
                "y"     : y,
                "sts"   : " ",
                "barco" : False,
                "tiro"  : False
            }

            linha.append(tile)
        pos["x"] = 0
        pos["y"] += 1
        grid.append(linha)

def printGrade():
    global gridInfo
    global grid
    global coord
    clear()
    print(f"Barcos restantes: {gridInfo['barcos']}\n")

    print("    ", end="")
    for i in range(gridInfo["width"]):
        print(coord[i], end=" ")
    print("\n  +", end="")
    print("-" * gridInfo["width"] * 2, end="")
    print("-+")

    for i in range(gridInfo["height"]):
        for j in range(gridInfo["width"]):
            end = " "
            if (grid[i][j]["x"] == gridInfo["width"] -1):
                end = " |\n"
            if (grid[i][j]["x"] == 0):
                print(f"{i + 1} | ", end="")

            #desenhar o barco (apagar depois)
            #if (grid[i][j]["barco"] == True):
            #    grid[i][j]["sts"] = "o"

            print(grid[i][j]["sts"], end=end)
    print("  +", end="")
    print("-" * gridInfo["width"] * 2, end="")
    print("-+")

def jogar():
    global grid
    global gridInfo
    global coord

    while True:
        if (gridInfo["barcos"] == 0):
            print("Você ganhou!")
            exit()

        try:
            jogada = input("Insira a coordenada (letra x número) ou '-1' para sair: ")
            if (jogada == "-1"):
                break
        except:
            print("Erro")
            continue
        else:
            try:
                for i in range(len(coord)):
                    if (jogada[:-1] == coord[i]):
                        x = i
                
                y = int(jogada[1])

                for i in range(gridInfo["height"]):
                    for j in range(gridInfo["width"]):
                        if (grid[i][j]["x"] == x) and (grid[i][j]["y"] == y - 1) and (grid[i][j]["tiro"] == False):   #mudar o desenho do tile atingido
                            grid[i][j]["tiro"] = True           #impede que o mesmo tile seja atingido novamente
                            if (grid[i][j]["barco"] == True):   #se houver um barco
                                grid[i][j]["sts"] = "x"         #mudar o desenho para um X
                                grid[i][j]["barco"] = False     #destruir o barco
                                gridInfo["barcos"] -= 1         #diminuir a quantidade de barcos na grade
                            else:
                                grid[i][j]["sts"] = "."         #se não tiver um barco, exibir um ponto
                            clear()
                            printGrade()
            except:
                print("Erro")
                continue

def nBarco(comprimento):
    global grid
    global gridInfo 

    barco = {
        "x" : [],
        "y" : []
    }

    pivoX = rand(0, gridInfo["width"] - comprimento)
    pivoY = rand(0, gridInfo["height"] - comprimento)

    rotacao = rand(0, 1)    #definir se o barco estará na vertical ou não (0 = não, 1 = sim)

    while (pivoX + comprimento >= gridInfo["width"]):
        pivoX -= 1

    for i in range(comprimento):
        if (rotacao == True):
            barco["x"].append(pivoX)
            barco["y"].append(pivoY + i)
        else:
            barco["x"].append(pivoX + i)
            barco["y"].append(pivoY)

    for i in range(gridInfo["height"]):                                                                 #varrer todas as linhas da grade
        for j in range(gridInfo["width"]):                                                              #varrer todas as colunas da grade
            for x in range(len(barco["x"])):                                                            #varrer as linhas do barco
                for y in range(len(barco["y"])):                                                        #varrer as colunas do barco
                    if (grid[i][j]["x"] == barco["x"][x]) and (grid[i][j]["y"] == barco["y"][y]) and (grid[i][j]["barco"] == False):       #se a posição X e Y do tile na grade coincidir com a posição X e Y do barco
                        grid[i][j]["barco"] = True
                        gridInfo["barcos"] += 1

def criarBarco():
    global grid
    global gridInfo



    '''
        comprimento     |       quantidade
            4           |           1
            3           |           2
            2           |           3
            1           |           4
    '''

    nBarco(4)
    for i in range(2):
        nBarco(3)
    for i in range(3):
        nBarco(2)
    for i in range(4):
        nBarco(1)


criarGrade()
criarBarco()
printGrade()
jogar()

