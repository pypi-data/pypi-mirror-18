from math import sqrt, cos, acos, exp, log, pi
from database import BdD


class VDW(object):
    """docstring for vdW"""
    def __init__(self):
        super(VDW, self).__init__()

    # T e P independentes
    def TP(self,T,P,componente):
        
        # Constantes caracteristicas
        from config_VDW import conf
        R, Omega_a, Omega_b = conf()
        Tc,Pc = BdD.get_dados(componente,ret=[0,1])
        
        # Proriedades reduzidas
        Tr, Pr = T/Tc, P/Pc
        
        # Calculo das constantes A*=A_ e B*=B_
        A_  = Omega_a*Pr/Tr**2
        B_  = Omega_b*Pr/Tr
        
        # Coeficientes da equacao cubica
        A = [-A_*B_, A_,-(B_ + 1)]
        
        # Solucao analitica
        Q_2 = (A[0]+2*A[2]**3/27-A[2]*A[1]/3)/2
        P_3 = (3*A[1]-A[2]**2)/9
        Delta = P_3**3 + Q_2**2

        if Delta >= 0:
            u = (-Q_2+sqrt(Delta))**(1/3)
            v = -P_3/u
            x1 = -A[2]/3 + u + v

            # Fator de compressibilidade
            Z = x1
            V = Z*R*T/P
            return {'Z':Z,'V':V}

        else:
            Phi = acos(-Q_2/sqrt(-P_3**3))
            x1 = -A[2]/3 + 2*sqrt(-P_3)*cos(Phi/3)
            x2 = -A[2]/3 + 2*sqrt(-P_3)*cos((Phi-pi)/3)
            x3 = -A[2]/3 + 2*sqrt(-P_3)*cos((Phi+pi)/3)
            
            # Fator de compressibilidade
            Zv, Zl = max(x1,x2,x3), min(x1,x2,x3)
            Vv = Zv*R*T/P
            Vl = Zl*R*T/P
            return {'Zv':Zv,'Zl':Zl,'Vv':Vv,'Vl':Vl}

    # T e V independentes
    def TV(T,V,componente):
        
        from config_VDW import conf 
        R = conf()[0]
        Tc,Pc = BdD.get_dados(componente,ret=[0,1])
        Alpha = Alpha_r = Alpha_c = 1
        
        # cálculo das constantes características ac, b, a
        ac = Omega_a*R**2*Tc**2/(Alpha_c*Pc)
        b = Omega_b*R*Tc/Pc
        a = ac*Alpha
        
        # cálculo da pressão em bar
        P = R*T/(V - b) - a/V**2
        
        # cálculo do fator de compressibilidade
        Z = P*V/(R*T)
        return {'Z':Z,'P':P}

    def Tboyle(self,componente):
        from config_VDW import conf
        Omega_a, Omega_b = conf()[1:]
        Tc = BdD.get_dados(componente,ret=[1])[0]
        Tboyle_r = Omega_a/Omega_b
        Tboyle = Tboyle_r*Tc
        return {'Tboyle':Tboyle}

class RK_MOD(object):
    """docstring for RK_MOD"""
    def __init__(self):
        super(RK_MOD, self).__init__()
    
    def baseTP(T,P,componente,Alpha_r):
        from config_RK_MOD import conf
        R,Omega_a,Omega_b = conf()        
        Tc,Pc,w = BdD.get_dados(componente,ret=[0,1,3])
        # propriedadede reduzida
        Tr, Pr = T/Tc, P/Pc
        
        # cálculo dos parâmetros adimensinais
        A_ = Pr*Alpha_r*Omega_a/Tr**2 
        B_ = Pr*Omega_b/Tr

        # Coeficientes da equacao cubica
        A = [-A_*B_, A_-B_**2-B_, -1]
        
        # Solucao analitica
        Q_2 = (A[0]+2*A[2]**3/27-A[2]*A[1]/3)/2
        P_3 = (3*A[1]-A[2]**2)/9
        Delta = P_3**3 + Q_2**2

        if Delta >= 0:
            Aux = Q_2+sqrt(Delta)

            if Aux > 0:
                v = -(Aux**(1/3))
                u = -P_3/v
            else:
                u = (-Q_2+sqrt(Delta))**(1/3)
                v = (-Aux)**(1/3)

            x1 = -A[2]/3 + u + v

            # Fator de compressibilidade
            Z = x1
            V = Z*R*T/P

            # fugacidade
            ln_Phi, Phi, f = RK_MOD.coef_fug(Z,P,A_,B_)

            return {'Z':Z,'V':V,'lncf':ln_Phi,'cf':Phi,'f':f}

        else:
            Phi = acos(-Q_2/sqrt(-P_3**3))
            x1 = -A[2]/3 + 2*sqrt(-P_3)*cos(Phi/3)
            x2 = -A[2]/3 + 2*sqrt(-P_3)*cos((Phi-pi)/3)
            x3 = -A[2]/3 + 2*sqrt(-P_3)*cos((Phi+pi)/3)
            
            # Fator de compressibilidade
            Zv = max(x1,x2,x3) 
            Zl = min(x1,x2,x3)
            Vv = Zv*R*T/P
            Vl = Zl*R*T/P

            # fase vapor
            ln_Phi_v, Phi_v, f_v = RK_MOD.coef_fug(Zv,P,A_,B_)

            # fase líquida
            ln_Phi_l, Phi_l, f_l = RK_MOD.coef_fug(Zl,P,A_,B_)

            return {'Z':[Zv, Zl],'V':[Vv,Vl],'lncf':[ln_Phi_v,ln_Phi_l],
            'cf':[Phi_v,Phi_l],'f':[f_v,f_l]}

    def baseTV(T,V,componente,Alpha,Alpha_c):
        from config_RK_MOD import conf
        R, Omega_a,Omega_b = conf()
        Tc,Pc,w = BdD.get_dados(componente,ret=[0,1,3])
        
        # propriedadede reduzida
        Tr = T/Tc
        
        # constantes caracteristicas
        ac = Omega_a*(R*Tc)**2/(Alpha_c*Pc)
        b = Omega_b*R*Tc/Pc
        a = ac*Alpha

        # calculo da pressão em bar
        P = R*T/(V-b)-a/(V*(V+b))

        # fator de compressibilidade
        Z = P*V/(R*T)

        return {'P':P,'Z':Z}

    def coef_fug(Z,P,A_,B_):
        # Parâmetro Aux1 e Aux2
        Aux1 = log(Z/(Z-B_))
        Aux2 = A_/B_*log(Z/(Z+B_))

        # Logaritmo do coef. de fugacidade
        ln_Phi = Aux1 + Aux2 + (Z - 1) - log(Z)
        
        # coef de fugacidade
        Phi = exp(ln_Phi)

        # fugacidade
        f = Phi*P

        return ln_Phi, Phi, f

    def RK_TP(self,T,P,componente):
        # propriededades físicas da substância
        Tc = BdD.get_dados(componente,ret=[1])[0]

        # constantes características e R:
        from config_RK_MOD import conf
        R,Omega_a,Omega_b = conf()

        # propriedadede reduzida
        Tr = T/Tc

        # cálculo do parâmetro Alpha
        Alpha_r = 1/sqrt(Tr)

        return RK_MOD.baseTP(T,P,componente,Alpha_r)

    def RK_TV(self,T,V,componente):
        # propriededades físicas da substância
        Tc = BdD.get_dados(componente,ret=[1])[0]

        # constantes características e R:
        from config_RK_MOD import conf
        R,Omega_a,Omega_b = conf()

        # propriedadede reduzida
        Tr = T/Tc

        # cálculo dos parâmetros Alpha
        Alpha_c = 1/sqrt(Tc)
        Alpha = 1/sqrt(T)

        return RK_MOD.baseTV(T,V,componente,Alpha,Alpha_c)

    def wilson_TP(self,T,P,componente):
        # propriededades físicas da substância
        Tc,w= BdD.get_dados(componente,ret=[0,3])

        # constantes características e R:
        from config_RK_MOD import conf
        R,Omega_a,Omega_b = conf()

        # propriedadede reduzida
        Tr = T/Tc

        # cálculo do parâmetro Alpha
        m = 1.57 + 1.62*w
        Alpha_r = Tr*(1+m*(1/Tr-1))

        return RK_MOD.baseTP(T,P,componente,Alpha_r)

    def wilson_TV(self,T,V,componente):
        # propriededades físicas da substância
        Tc,w = BdD.get_dados(componente,ret=[0,3])

        # constantes características e R:
        from config_RK_MOD import conf 
        R,Omega_a,Omega_b = conf()

        # propriedadede reduzida
        Tr = T/Tc

        # cálculo dos parâmetros Alpha
        m = 1.57 + 1.62*w
        Alpha = Tr*(1+m*(1/Tr-1))
        Alpha_c = 1
        return RK_MOD.baseTV(T,V,componente,Alpha,Alpha_c)

    def SRK_TP(self,T,P,componente):
        # propriededades físicas da substância
        Tc,w= BdD.get_dados(componente,ret=[0,3])

        # constantes características e R:
        from config_RK_MOD import conf
        R, Omega_a,Omega_b = conf()

        # propriedadede reduzida
        Tr = T/Tc

        # cálculo do parâmetro Alpha
        m = 0.480 + 1.574*w - 0.176*w**2 
        Alpha_r = (1+m*(1-sqrt(Tr)))**2

        return RK_MOD.baseTP(T,P,componente,Alpha_r)

    def SRK_TV(self,T,V,componente):
        Tc,w = BdD.get_dados(componente,ret=[0,3])

        # constantes características e R:
        from config_RK_MOD import conf
        R, Omega_a,Omega_b = conf()

        # propriedadede reduzida
        Tr = T/Tc

        # cálculo dos parâmetros Alpha
        m = 0.480 + 1.574*w - 0.176*w**2 
        Alpha = (1+m*(1-sqrt(Tr)))**2
        Alpha_c = 1
        return RK_MOD.baseTV(T,V,componente,Alpha,Alpha_c)

class PR_MOD(object):
    """docstring for PR_MOD"""
    def __init__(self):
        super(PR_MOD, self).__init__()
    
    def baseTP(T,P,componente,Alpha_r):
        from config_PR_MOD import conf
        R, Omega_a, Omega_b = conf()
        Tc,Pc = BdD.get_dados(componente,ret=[0,1])
        # propriedades reduzidas
        Tr = T/Tc
        Pr = P/Pc
        # calculo dos parametros reduzidos
        A_ = Omega_a*Alpha_r*Pr/Tr**2
        B_ = Omega_b*Pr/Tr
        # calculo dos coeficentes da equacao cubica
        A = [B_**3+B_**2-A_*B_, -(3*B_**2+2*B_-A_), B_-1]        
        # Solucao analitica
        Q_2 = (A[0]+2*A[2]**3/27-A[2]*A[1]/3)/2
        P_3 = (3*A[1]-A[2]**2)/9
        Delta = P_3**3 + Q_2**2
        if Delta >= 0:
            u = (-Q_2+sqrt(Delta))**(1/3)
            v = -P_3/u
            x1 = -A[2]/3 + u + v
            # Fator de compressibilidade
            Z = x1
            V = Z*R*T/P
            return {'Z':Z,'V':V}
        else:
            Phi = acos(-Q_2/sqrt(-P_3**3))
            x1 = -A[2]/3 + 2*sqrt(-P_3)*cos(Phi/3)
            x2 = -A[2]/3 + 2*sqrt(-P_3)*cos((Phi-pi)/3)
            x3 = -A[2]/3 + 2*sqrt(-P_3)*cos((Phi+pi)/3)
            
            # Fator de compressibilidade
            Zv, Zl = max(x1,x2,x3), min(x1,x2,x3)
            Vv = Zv*R*T/P
            Vl = Zl*R*T/P
            return {'Zv':Zv,'Zl':Zl,'Vv':Vv,'Vl':Vl}


    def baseTV(T,P,comp):
        pass

    def coef_fug(Z,P,A_,B_):
        # Parâmetro Aux1 e Aux2
        Aux1 = log(Z/(Z-B_))
        Aux2 = A_/B_*log(Z/(Z+B_))

        # Logaritmo do coef. de fugacidade
        ln_Phi = Aux1 + Aux2 + (Z - 1) - log(Z)
        
        # coef de fugacidade
        Phi = exp(ln_Phi)

        # fugacidade
        f = Phi*P

        return ln_Phi, Phi, f


    def PR_TP(self,T,P,componente):
        Tc,w = BdD.get_dados(componente,ret=[0,3])
        Tr = T/Tc
        m = 0.37464 + 1.54226*w - 0.26992*w**2
        Alpha = (1 + m*(1-sqrt(Tr)))**2
        return PR_MOD.baseTP(T,P,componente,Alpha)

class BWRS(object):
    """docstring for BWRS"""

    def __init__(self):
        super(BWRS, self).__init__()

    
    def parametros(T,componente):
        from config_BWRS import conf
        R,A,B = conf()
        Tc,Pc,Vc,w = BdD.get_dados(componente,ret=[0,1,2,3])

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
        Alpha = (A[6]+B[6]*w)*Vc**3 #(cm9/mol3)
        Gamma = (A[3]+B[3]*w)*Vc**2 #(cm6/mol2)

        # cálculo dos parâmetros K1, K2, K3 e K4
        K1 = B0*R*T-A0-C0/T**2+D0/T**3-E0/T**4
        K2 = b*R*T-a-d/T
        K3 = Alpha*(a+d/T)
        K4 = c/T**2

        return A0,B0,C0,D0,E0,a,b,c,d,Alpha,Gamma,K1,K2,K3,K4,Tc

    # BWRS para T e V independentes
    def TV(self,T,V,componente):
        from config_BWRS import conf
        R,A,B = conf()
        A0,B0,C0,D0,E0,a,b,c,d,Alpha,Gamma,K1,K2,K3,K4,Tc = BWRS.parametros(T,componente)
        
        # Os coeficientes calculados aqui são variáveis locais
        rho = 1/V
        A1 = R*T*rho
        A2 = K1*rho**2 
        A3 = K2*rho**3
        A4 = K3*rho**6
        A5 = K4*rho**3*(1+Gamma*rho**2)*exp(-Gamma*rho**2)
        P = A1 + A2 + A3 + A4 + A5
        Z = P*V/(R*T)
        return (P,Z) 

    # BWRS para T e P independentes
    def TP(self,T,P,componente,fase='vapor',Itemax=100,Tol=1e-10):

        from config_BWRS import conf
        R,A,B = conf()
        A0,B0,C0,D0,E0,a,b,c,d,Alpha,Gamma,K1,K2,K3,K4,Tc = BWRS.parametros(T,componente)

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
            # cálculo dos coeficientes Omega_
            Omega_1 = K1/(R*T)*rho
            Omega_2 = K2/(R*T)*rho**2
            Omega_3 = K3/(R*T)*rho**5
            Omega_4 = K4/(R*T)*rho**2*(1+Gamma*rho**2)\
            *exp(-Gamma*rho**2)
            # cálculo da função objetivo
            F = 1+Omega_1+Omega_2+Omega_3+Omega_4-Z
            # convergência
            L[0] = Ite>Itemax
            L[1] = abs(F)<Tol and abs(Z-Z0)<Tol
            if L[0] or L[1]: break
            # cálcular as derivadas
            d_Omega_1 = -Omega_1/Z
            d_Omega_2 = -2*Omega_2/Z
            d_Omega_3 = -5*Omega_3/Z
            d_Omega_4 = K4/(R*T)*(-2*rho**2-4*Gamma*rho**4)/Z*exp(-Gamma*rho**2)\
            +Omega_4*(2*Gamma*rho**2)/Z
            dF = d_Omega_1+d_Omega_2+d_Omega_3+d_Omega_4-1
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
    def Virial_23(self,T,componente):
        
        from config_BWRS import conf
        R,A,B = conf()
        A0,B0,C0,D0,E0,a,b,c,d,Alpha,Gamma,K1,K2,K3,K4,Tc = BWRS.parametros(T,componente)
        
        B = K1/(R*T)
        C = (K2 + K4)/(R*T)
        return {'B':B, 'C':C}
    
    # cálculo da temperatura de Boyle
    def Tboyle(self,T,componente,fase='vapor',Itemax=100,Tol=1e-10,Tr=3):
        from config_BWRS import conf
        R,A,B = conf()
        A0,B0,C0,D0,E0,a,b,c,d,Alpha,Gamma,K1,K2,K3,K4,Tc = BWRS.parametros(T,componente)
        # cálculo dos coeficientes da função objetivo
        Aux0 = -E0/(B0*R*Tc**5)
        Aux1 = -D0/(B0*R*Tc**4)
        Aux2 = -C0/(B0*R*Tc**3)
        Aux4 = -A0/(B0*R*Tc)
        # Inicialização das variáveis de controle do processo iterativo
        T0 = float('inf')
        Ite = 1
        L = [False, False]
        # método de newton raphson
        while True:
            # função objetivo
            F = Tr**5 + Aux4*Tr**4 + Aux2*Tr**2 \
            + Aux1*Tr + Aux0
            L[0] = Ite>Itemax
            L[1] = abs(F)<Tol or abs(Tr-T0)<Tol
            if L[0] or L[1]: break
            dF = 5*Tr**4 + 4*Aux4*Tr**3 + 2*Aux2*Tr\
            + Aux1
            if abs(dF)<Tol:break
            T0 = Tr
            Tr = Tr - F/dF
            Ite += 1
            
        T_boyle = Tc*Tr

        return {'Tboyle':T_boyle}


if __name__ == '__main__':
    teste1 = BWRS()
    teste2 = VDW()
    teste3 = RK_MOD()
    teste4 = PR_MOD()

    comp = 'carbon dioxide'
    comp2 = 'carbon dioxide'
    T = 473.15
    T2 = 283.15
    P = 40
    P2 = None
    V = None
    V2 = 1250

    print('-----------------Dados de Entrada(TP)----------------')
    print('T:{0:.2f} (K) | P:{1:.2f} (bar) | Componente: {2}\n'.format(T,P,comp))
    print('-----------Resultado(T e P independentes)------------')
    # TP
    resultado1 = teste1.TP(T,P,comp)
    resultado2 = teste2.TP(T,P,comp)
    resultado3 = teste3.RK_TP(T,P,comp)
    resultado4 = teste3.wilson_TP(T,P,comp)
    resultado5 = teste3.SRK_TP(T,P,comp)
    resultado6 = teste4.PR_TP(T,P,comp)

    print('  BWRS: Z:{0:.4f}  V:{1:.4f}'.format(resultado1['Z'],resultado1['V']))
    print('   VDW: Z:{0:.4f}  V:{1:.4f}'.format(resultado2['Z'],resultado2['V']))
    print('    RK: Z:{0:.4f}  V:{1:.4f}  ln_Phi:{2:.4f}'.format(resultado3['Z'],resultado3['V'],resultado3['lncf']))
    print('WILSON: Z:{0:.4f}  V:{1:.4f}  ln_Phi:{2:.4f}'.format(resultado4['Z'],resultado4['V'],resultado4['lncf']))
    print('   SRK: Z:{0:.4f}  V:{1:.4f}  ln_Phi:{2:.4f}'.format(resultado5['Z'],resultado5['V'],resultado5['lncf']))
    print('    PR: Z:{0:.4f}  V:{1:.4f}'.format(resultado6['Z'],resultado6['V']))
    
    # # TV
    print('\n\n----------------Dados de Entrada(TV)-----------------')
    print('T:{0:.2f} (K) | V:{1:.2f} (cm3/mol) | Componente: {2}\n'.format(T2,V2,comp2))
    print('-----------Resultado(T e V independentes)------------')
    resultado3 = teste3.RK_TV(T2,V2,comp2)
    resultado4 = teste3.wilson_TV(T2,V2,comp2)
    resultado5 = teste3.SRK_TV(T2,V2,comp2)

    print('    RK: Z:{0:.4f}  P:{1:.4f}'.format(resultado4['Z'],resultado4['P']))
    print('WILSON: Z:{0:.4f}  P:{1:.4f}'.format(resultado3['Z'],resultado3['P']))
    print('   SRK: Z:{0:.4f}  P:{1:.4f}'.format(resultado5['Z'],resultado5['P']))
    
