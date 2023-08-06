'''
Função usada para imprimir uma lista no python
função print_lista recebe 3 valores
    1º lista que será impressa
    2º não obrigatorio a True ou False para a identação da lista
    3º não obrigatorio o avanço do texto
'''


def print_lista(lista, identa=True, avanco=0):
    for x in lista:
        if isinstance(x, list):
            print_lista(x, identa, avanco+1)
        else:
            if identa:
                for l in range(avanco):
                    print("\t", end='')
            print(x)

