import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def clamp(n, min, max):
    if (n < min):
        return min
    elif (n > max):
        return max
    return n

from random import randint as rand

#informações sobre as dimensões da grade
gridInfo = {
    "width"     : 10,
    "height"    : 7,
    "barcos"    : 0
}

gridInfo["width"] = clamp(gridInfo["width"], 9, 26)
gridInfo["height"] = clamp(gridInfo["height"], 9, 9)

#array com as coordenadas do eixo X
coord = "abcdefghijklmnopqrstuvwxyz"

def criarGrade(width, height):
    #criar grade, da esquerda pra direita, de cima pra baixo
    mat = []
    for i in range(height):
        mat.append([0] * width)
    return mat

def printGrade():
    global gridInfo
    global grid
    global coord
    clear()

    #(vazio, navio, erro, acerto)
    sts = "  .x"

    print(f"Barcos restantes: {gridInfo['barcos']}\n")

    print("    ", end="")
    for i in range(gridInfo["width"]):
        print(coord[i], end=" ")
    print("\n  +", end="")
    print("-" * gridInfo["width"] * 2, end="")
    print("-+")

    for i in range(gridInfo["height"]):
        print(i, end=" | ")
        for j in range(gridInfo["width"]):
            print(sts[grid[i][j]], end=" ")
        print("|")
        
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
                for i in range(len(grid)):
                    print(grid[i])
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


                if grid[y][x] == 0: #jogador errou e acertou no mar
                    grid[y][x] = 2

                if grid[y][x] == 1: #jogador acertou a célula de um navio
                    grid[y][x] = 3
                    gridInfo["barcos"] -= 1

                clear()
                printGrade()
            except:
                print("Erro")
                continue

def checaBarco(rotacao, comprimento, pivoX, pivoY):
    global grid
    margin = 1

    #verificar se o espaço do barco está vazio e com uma margem de uma célula de outros barcos
    if rotacao == 1:
        for y in range(pivoY - margin, pivoY + comprimento + margin):
            for x in range(pivoX - margin, pivoX + margin + 1):
                try:
                    if grid[y][x] > 0:
                        return False
                except:
                    continue

    if rotacao == 0:
        for y in range(pivoY - margin, pivoY + margin + 1):
            for x in range(pivoX - margin, pivoX + comprimento + margin):
                try:
                    if grid[y][x] > 0:
                        return False
                except:
                    continue
    return True

def nBarco(comprimento):
    global grid
    global gridInfo 

    #tentar 1000 vezes encaixar os barcos na grade
    for i in range(1000):
        rotacao = rand(0, 1)    #definir se o barco estará na vertical ou não (0 = não, 1 = sim)
        #rotacao = 0
        pivoX = rand(0, gridInfo["width"] - comprimento)
        pivoY = rand(0, gridInfo["height"] - comprimento)

        if checaBarco(rotacao, comprimento, pivoX, pivoY):
            break
    
    for i in range(comprimento):
        if (rotacao == True):
            grid[pivoY + i][pivoX] = 1
        else:
            grid[pivoY][pivoX + i] = 1

        gridInfo["barcos"] += 1


def criarBarco():
    nBarco(4)
    for i in range(2):
        nBarco(3)
    for i in range(3):
        nBarco(2)
    for i in range(4):
        nBarco(1)


grid = criarGrade(gridInfo["width"], gridInfo["height"])
criarBarco()
printGrade()
jogar()
