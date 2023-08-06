class BdD(object):
    """docstring for BdD"""
    def __init__(self):
        super(BdD, self).__init__()


    def get_dados(componente,ret=None):
        import csv
        # Name;Formula;MW;Tc;Pc;Vc;Rho_c;Zc;w
        # alocando espaço para as listas

        with open('DadosCriticos.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile,delimiter=';')

            # Atribuindo os valores as listas
            Nome = []
            Formula = []
            Dados = []
            
            for row in csvreader:
                Nome.append(row[0])
                Formula.append(row[1])
                Dados.append(row[2:])
        
        try:
            I = Nome.index(componente)
        except ValueError: 
            try:
                I = Formula.index(componente)
            except ValueError:
                print('Componente fora do banco de dados')
                exit(1)
        
        saida = []
        for j in ret:
            try:
                saida.append(float(Dados[I][j]))
            except ValueError:
                print('Dados incompletos no banco de dados')
                exit(1)
        return saida