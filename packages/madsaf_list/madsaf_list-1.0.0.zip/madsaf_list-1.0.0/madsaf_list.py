"""Esse módulo nester.py fornece um função chamada print_lol que permite processar e imprimir uma lista ela estando aninhadas ou não."""
import sys

def print_lol(the_list, indent=False, level=0, fh=sys.stdout):

    """Essa função requer um argumento posicional chamado "the_list", que é qualquer lista em python. Cada item de dados na lista fornecida é
(recursivamente) impresso na tela em sua propria linha e o argumento "level" que determina a tabulação de cada aninhamento"""
    
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1, fh)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='', file = fh)
            print(each_item, file = fh)

            
