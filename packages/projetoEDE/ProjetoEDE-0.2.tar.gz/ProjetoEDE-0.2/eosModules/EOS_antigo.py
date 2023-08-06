from math import*

class equacoes_de_estado(object):
    """Classe das equacoes de estado"""
    def __init__(self):
        super(equacoes_de_estado, self).__init__()

    def van_der_walls(self,T,P=None,V=None,Tc=None,Pc=None,
        componente=[],flags=[]):
        # Constantes caracteristicas
        Omega_a = 27/64
        Omega_b = 1/8

        # verificar se o componente foi informado e importa os dados
        if componente:
            from DB import banco_de_dados 
            I, Name, Formula, Mw, Tc, Pc, Vc, Rho_c, Zc, w = \
            banco_de_dados.get_dados(self,componente)
            try:
                Tc = float(Tc[I])
                Pc = float(Pc[I])
            except ValueError:
                print('Dados ausentes do banco no dados. Por favor, informe Tc,Pc e w')
                exit(1) 
        elif not any((Tc,Pc)):
            print('Informe a identificação do componente ou os dados cŕiticos')
            exit(1)

        # Proriedades reduzidas
        Tr, Pr, alpha_r = T/Tc, P/Pc, 1

        # T e P independentes
        def vdW_TP():
            # Calculo das constantes A* e B*
            A_star  = Omega_a*Pr/Tr**2
            B_star  = Omega_b*Pr/Tr
            # Coeficientes da equacao cubica
            A = [-A_star*B_star, A_star,-(B_star + 1)]
            # Solucao analitica
            Q_sobre_2 = (A[0]+2*A[2]**3/27-A[2]*A[1]/3)/2
            P_sobre_3 = (3*A[1]-A[2]**2)/9
            delta = P_sobre_3**3 + Q_sobre_2**2

            if delta >= 0:
                u = (-Q_sobre_2+sqrt(delta))**(1/3)
                v = -P_sobre_3/u
                x1 = -A[2]/3 + u + v

                # Fator de compressibilidade
                Zv = x1
                return Zv

            else:
                phi = acos(-Q_sobre_2/sqrt(-P_sobre_3**2))
                x1 = -A[2]/3 + 2*sqrt(-P_sobre_3)*cos(phi/3)
                x2 = -A[2]/3 + 2*sqrt(-P_sobre_3)*cos((phi-pi)/3)
                x3 = -A[2]/3 + 2*sqrt(-P_sobre_3)*cos((phi+pi)/3)
                
                # Fator de compressibilidade
                Zv, Zl = max(x1,x2,x3), min(x1,x2,x3)
                return Zv, Zl

        # T e V independentes
        def vdW_TV():
            R = 83.144
            alpha = alpha_r = alpha_c = 1
            # cálculo das constantes características ac, b, a
            ac = Omega_a*R**2*Tc**2/(alpha_c*Pc)
            b = Omega_b*R*Tc/Pc
            a = ac*alpha
            # cálculo da pressão em bar
            P = R*T/(V - b) - a/V**2
            # cálculo do fator de compressibilidade
            Z = P*V/(R*T)
            return {'Z':Z,'P':P}

        def verifica_estabilidade():
            pass

        
        # teste/ deletar depois
        teste = vdW_TP()
        print(teste)

    def BWRS(self,T,P,componente=None,Tc=None,Vc=None,w=None,
        rho=None,Itemax=100,Tol=1e-8,fase='vapor',flags=[]):
        

        #------------------------A-------------------------------
        R=83.144
        A = (0.443690, 1.284380, 0.356306, 0.544979, 0.528629\
        , 0.484011, 0.0705233, 0.504087, 0.0307452, 0.0732828\
        , 0.006450)
        

        # -----------------------B------------------------------
        B = (0.115449, -0.920731, 1.70871, -0.270896, 0.349261\
        , 0.75413, -0.044448, 1.32245, 0.179433, 0.463492\
        ,-0.022143)

        # verificar se o componente foi informado e importa os dados
        # codigo ret: MW=0; Tc=1; Pc=2; Vc=3; Rho_c=4; Zc=5; w=6
        if componente:
            from DB import banco_de_dados 
            Tc,Vc,w = banco_de_dados.get_dados(self,componente,ret=[1,3,6])
        elif not any((Tc,Vc,w)):
            print('Informe o componente ou os dados cŕiticos(Tc,Vc) e w.')
            exit(1)

        # cálculo dos parâmetros caracteristicos de cada substância
        A0 = (A[1]+B[1]*w)*R*Tc*Vc #(bar.cm6/mol2)
        B0 = (A[0]+B[0]*w)*Vc #(cm3/mol)
        C0 = (A[2]+B[2]*w)*R*Tc**3*Vc #(bar.cm6.K2/mol2)
        D0 = (A[8]+B[8]*w)*R*Tc**4*Vc #(bar.cm6.K3/mol2)
        E0 = (A[10]+B[10]*w*exp(-3.8*w))*R*Tc**5*Vc #(bar.cm6.K4/mol2)
        a = (A[5]+B[5]*w)*R*Tc*Vc**2 #(bar.cm9/mol3)
        b = (A[4]+B[4]*w)*Vc**2 #(bar.cm9/mol3)
        c = (A[7]+B[7]*w)*R*Tc**3*Vc**2 #(bar.cm9.K2/mol3)
        d = (A[9]+B[9]*w)*R*Tc**2*Vc**2 #(bar.cm9.K/mol3)
        alpha = (A[6]+B[6]*w)*Vc**3 #(cm9/mol3)
        gamma = (A[3]+B[3]*w)*Vc**2 #(cm6/mol2)

        # cálculo dos parâmetros K1, K2, K3 e K4
        K1 = B0*R*T-A0-C0/T**2+D0/T**3-E0/T**4
        K2 = b*R*T-a-d/T
        K3 = alpha*(a+d/T)
        K4 = c/T**2

        # BWRS para estimar P
        def BWRS_TV():
            # Os coeficientes calculados aqui são variáveis locais
            A1 = R*T*rho
            A2 = K1*rho**2 
            A3 = K2*rho**3
            A4 = K3*rho**6
            A5 = K4*rho**3*(1+gamma*rho**2)*exp(-gamma*rho**2)
            P = A1 + A2 + A3 + A4 + A5
            Z = P/(rho*R*T)
            return (P,Z) 

        # BWRS para T e P independentes
        def BWRS_TP():

            # estimativa inicial
            if fase == 'vapor':
                Z = 1
            elif fase == 'liquido':
                Z = 0.003
            else:
                print('As fases devem ser: liquido ou vapor')
                exit(1)

            # inicialização das ariáveis de controle do processo iterativo: 
            Z0 = float('inf')
            Ite = 1
            L = [False, False, False]

            # método de newton-raphson
            while True:
                # densidade molar através da presão
                rho = P/(Z*R*T)
                # cálculo dos coeficientes omega
                omega1 = K1/(R*T)*rho
                omega2 = K2/(R*T)*rho**2
                omega3 = K3/(R*T)*rho**5
                omega4 = K4/(R*T)*rho**2*(1+gamma*rho**2)\
                *exp(-gamma*rho**2)
                # cálculo da função objetivo
                F = 1+omega1+omega2+omega3+omega4-Z
                # convergência
                L[0] = Ite>Itemax
                L[1] = abs(F)<Tol and abs(Z-Z0)<Tol
                if L[0] or L[1]: break
                # cálcular as derivadas
                d_omega1 = -omega1/Z
                d_omega2 = -2*omega2/Z
                d_omega3 = -5*omega3/Z
                d_omega4 = K4/(R*T)*(-2*rho**2-4*gamma*rho**4)/Z*exp(-gamma*rho**2)\
                +omega4*(2*gamma*rho**2)/Z
                dF = d_omega1+d_omega2+d_omega3+d_omega4-1
                L[2] = abs(dF)<1e-20
                if L[2]: break #verificando pontos de mínimo ou máximo
                # cálcular um novo valor para Z via método de Newton-Raphson
                Z0 = Z
                Z = Z-F/dF
                Ite = Ite+1

            # cálculo do volume molar em cm3/mol
            V = Z*R*T/P
            return {'Z':Z, 'V':V}   
            
        # cálculo do segundo e terceiro coeficiente do virial
        def Virial_23():
            B = K1/(R*T)
            C = (K2 + K4)/(R*T)
            return (B, C)
        
        # cálculo da temperatura de Boyle
        def Boyle_T(Tr=3):
            # cálculo dos coeficientes da função objetivo
            lambda0 = -E0/(B0*R*Tc**5)
            lambda1 = -D0/(B0*R*Tc**4)
            lambda2 = -C0/(B0*R*Tc**3)
            lambda4 = -A0/(B0*R*Tc)
            # Inicialização das variáveis de controle do processo iterativo
            T0 = float('inf')
            Ite = 1
            L = [False, False]
            # método de newton raphson
            while True:
                # função objetivo
                F = Tr**5 + lambda4*Tr**4 + lambda2*Tr**2 \
                + lambda1*Tr + lambda0
                L[0] = Ite>Itemax
                L[1] = abs(F)<Tol or abs(Tr-T0)<Tol
                if L[0] or L[1]: break
                dF = 5*Tr**4 + 4*lambda4*Tr**3 + 2*lambda2*Tr\
                + lambda1
                if abs(dF)<Tol:break
                T0 = Tr
                Tr = Tr - F/dF
                Ite += 1
            T_boyle = Tc*Tr
            return T_boyle

        # teste/ deletar depois
        return BWRS_TV()




    def BWRS_Mistura(self,T,P,componente=[],y=[],
        Tc=None,Vc=None,w=None,
        rho=None,
        Itemax=100,Tol=1e-8,fase='vapor'):

        R=83.144

        # verifica se a soma das composições = 1
        if y:
            if not sum(y)==1:
                print('Soma das composições diferente de 1 !!!')
                exit(1)

        # determinando a quandtidade de componentes na mistura
        n_comp = len(componente)

        # parâmetros binários (depois procurar um database disso)
        k=[]
        ki=[0]*n_comp
        for i in range(n_comp):
            k.append(ki)
        
        # utilizando o modulo BWRS para determinar as propriedades de cada substancia
        par=[]
        for composto in componente:
            par.append(equacoes_de_estado.BWRS(self,T,P,componente=composto,fase=fase))

        # regra de mistura para constantes caracteristicas
        # (A0,B0,C0,D0,E0,a,b,c,d,alpha,gamma)
        A0=B0=C0=D0=E0=a=b=c=d=alpha=gamma=0
        for i in range(n_comp):
            for j in range(n_comp):
                A0+=y[i]*y[j]*sqrt(par[i][0])*sqrt(par[j][0])*(1-k[i][j])
        for i in range(n_comp):
            B0+=y[i]*par[i][1]    
        
        for i in range(n_comp):
            for j in range(n_comp):
                C0+=y[i]*y[j]*sqrt(par[i][2])*sqrt(par[j][2])*(1-k[i][j])**3
        for i in range(n_comp):
            for j in range(n_comp):
                D0+=y[i]*y[j]*sqrt(par[i][3])*sqrt(par[j][3])*(1-k[i][j])**4
        for i in range(n_comp):
            for j in range(n_comp):
                E0+=y[i]*y[j]*sqrt(par[i][4])*sqrt(par[j][4])*(1-k[i][j])**5
        

        for i in range(n_comp):
                a+=(y[i]*par[i][5]**(1/3))
        for i in range(n_comp):
                b+=y[i]*par[i][6]**(1/3)
        for i in range(n_comp):
                c+=y[i]*par[i][7]**(1/3)        
        for i in range(n_comp):
                d+=y[i]*par[i][8]**(1/3)
        
        for i in range(n_comp):
                alpha+=y[i]*par[i][9]**(1/3)
        for i in range(n_comp):
                gamma+=y[i]*par[i][10]**(1/2)
        a **= 3
        b **= 3
        c **= 3
        d **= 3
        alpha **= 3
        gamma **= 2

        # cálculo dos parâmetros da mistura
        K1 = B0*R*T-A0-C0/T**2+D0/T**3-E0/T**4
        K2 = b*R*T-a-d/T
        K3 = alpha*(a+d/T)
        K4 = c/T**2

        A1 = R*T*rho
        A2 = K1*rho**2 
        A3 = K2*rho**3
        A4 = K3*rho**6
        A5 = K4*rho**3*(1+gamma*rho**2)*exp(-gamma*rho**2)
        P = A1 + A2 + A3 + A4 + A5
        Z = P/(rho*R*T)

        return{'Z':Z,'P':P}


if __name__ == '__main__':
    teste = equacoes_de_estado()

    # ---------------------------van_der_Walls-----------------------------
    # resultado = teste.van_der_walls(282.36,50.31999999999999,componente='ethylene')
    
    # ----------------------------BWRS-------------------------------------
    resultado = teste.BWRS(300, 40,componente='ethylene',fase='vapor',
     Itemax=50, Tol=1e-10, rho = 5e-3)
    print(resultado)
    # ----------------------------BWRS-Mistura------------------------------
    # resultado = teste.BWRS_Mistura(373.15,40,componente=['CH4','C4H10'],
    #     y=[0.50435, 0.49565],rho=1.251e-3)
    # print(resultado)