import sys
"""Este é o módulo "recursivefunc.py" que fornece uma função chamada print_lol()
que imprime listas que podem ou não incluir listas aninhadas."""
def print_lol(the_list,indent=False,level=0,fh=sys.stdout):
        """Esta função requer um argumento posicional chamado "the_list", que é qualquer lista Python (de possíveis listas aninhadas).
        Cada item de dados na lista fornecida é (recursivamente) impressso na tela em sua própria linha."""
        for each_item in the_list:
                        if isinstance(each_item,list):
                                print_lol(each_item,indent,level+1,fh)
                        else:
                                if indent:
                                        for tab_stop in range(level):
                                                print("\t",end="",file=fh)
                                print(each_item,file=fh)
