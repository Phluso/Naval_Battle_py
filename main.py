import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def printMenu():
    print("Binóculo: 1x\nAvião de Reconhecimento: 2x\nAvião de Ataque: 1x\nBomba Atômica: 1x")

def clamp(n, min, max):
    if (n < min):
        return min
    elif (n > max):
        return max
    return n

def lerp(a, b, t):
    return (1 - t) * a + t * b

from random import randint as rand

#informações sobre as dimensões da grade
gridInfo = {
    "width"     : 26,
    "height"    : 9,
    "barcos"    : 0
}

#gridInfo["width"] = clamp(gridInfo["width"], 9, 26)
#gridInfo["height"] = clamp(gridInfo["height"], 9, 9)

def criarGrade(width, height):
    #criar grade, da esquerda pra direita, de cima pra baixo
    mat = [0] * height
    for i in range(height):
        mat[i] = [0] * width

    return mat

def printGrade():
    global gridInfo
    global grid

    #(vazio, navio escondido, erro, acerto, navio revelado)
    sts = "  .xo"

    print(f"Barcos restantes: {gridInfo['barcos']}\n")

    print("    ", end="")
    for i in range(gridInfo["width"]):
        print("abcdefghijklmnopqrstuvwxyz"[i%26], end=" ")
    print("\n    +", end="")
    print("-" * gridInfo["width"] * 2, end="")
    print("-+")

    for i in range(gridInfo["height"]):
        print(f"{(i + 1): 3}", end=" | ")
        for j in range(gridInfo["width"]):
            print(sts[grid[i][j]], end=" ")
        print("|")
        
    print("    +", end="")
    print("-" * gridInfo["width"] * 2, end="")
    print("-+")

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
        clear()
        loadString = "|/-\\|/-\\"
        print(f"Posicionando barcos... {loadString[round(i/10)%8]}")
        rotacao = rand(0, 1)    #definir se o barco estará na vertical ou não (0 = não, 1 = sim)
        #rotacao = 0
        pivoX = rand(0, gridInfo["width"] - comprimento)
        pivoY = rand(0, gridInfo["height"] - comprimento)

        if checaBarco(rotacao, comprimento, pivoX, pivoY):
            break
    
    for i in range(comprimento):
        if rotacao:
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

def ataqueEspecial(posX, posY, atk):
    global grid
    global gridInfo

    #ataques:
    #binoculo, reconhecimento, ataque, bomba atomia

    if atk == 1:
        naviosDetectados = 0
        for i in range(len(grid[0])):
            posX = round(lerp(0, len(grid[0]), i / len(grid[0])))
            for y in range(-1, 2):
                try:
                    if grid[posY + y][posX] == 1:
                        grid[posY + y][posX] = 4
                        naviosDetectados += 1
                except:
                    pass
            clear()
            print(f"Procurando navios... {naviosDetectados} navios detectados até agora...")
            printGrade()

    if atk == 2:
        naviosDestruidos = 0
        for i in range(len(grid[0])):
            posX = round(lerp(0, len(grid[0]), i / len(grid[0])))
            if (grid[posY][posX] == 1) or (grid[posY][posX] == 4):
                grid[posY][posX] = 3
                naviosDestruidos += 1
                gridInfo["barcos"] -= 1
            else:
                grid[posY][posX] = 2
            clear()
            print(f"Atacando navios... {naviosDestruidos} navios destruídos até agora...")
            printGrade()

    if atk == 3:
        explosionRange = 7
        for i in range(10):
            for y in range(len(grid)):
                for x in range(len(grid[y])):
                    catetoX = x - round(posX)
                    catetoY = y - round(posY)

                    hipotenusa = round((catetoX**2 + catetoY**2)**.5)

                    if hipotenusa < lerp(0, explosionRange, i / 10):
                        if grid[y][x] == 0:
                            grid[y][x] = 2

                        if (grid[y][x] == 1) or (grid[y][x] == 4):
                            grid[y][x] = 3
                            gridInfo["barcos"] -= 1
            clear()
            printGrade()

def jogar():
    global grid
    global gridInfo

    while True:
        if (gridInfo["barcos"] == 0):
            print("Você ganhou!")
            exit()

        clear()
        printMenu()
        printGrade()

        try:
            jogada = input("'atk': ataque especial\nletra + número: jogada normal\n-1: sair\nEscolha uma opção: ")
            if (jogada == "-1"):
                break
        except:
            print("Erro")
            continue
        else:
            try:
                ataque = None
                #ataque especial
                if jogada == "atk":
                    try:
                        ataque = int(input("1- Avião de reconhecimento\n2- Avião de ataque\n3- Bomba atômica\nEscolha o ataque: "))
                        jogada = input("Insira as coordenadas (letra x número) do ataque: ")
                    except:
                        pass

                #capturar a coordenada X
                for i in range(len("abcdefghijklmnopqrstuvwxyz")):
                    if (jogada[:-1] == "abcdefghijklmnopqrstuvwxyz"[i]):
                        x = i
                
                #capturar a coordenada Y
                y = int(jogada[1]) -1

                if ataque == None:
                    #jogador errou e acertou no mar
                    if grid[y][x] == 0: 
                        grid[y][x] = 2

                    #jogador acertou a célula de um navio
                    if (grid[y][x] == 1) or (grid[y][x] == 4): 
                        grid[y][x] = 3
                        gridInfo["barcos"] -= 1

                    printGrade()
                else:
                    ataqueEspecial(x, y, ataque)
            except:
                print("Erro")
                continue

grid = criarGrade(gridInfo["width"], gridInfo["height"])

criarBarco()

'''for i in range(1, round(len(grid)/2)):
    ataqueEspecial(10, i * 2, 1)

for i in range(len(grid)):
    ataqueEspecial(10, i, 2)'''

jogar()





for i in range(len(grid)):
    print(grid[i])
