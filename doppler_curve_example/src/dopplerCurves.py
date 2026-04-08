import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
import pandas as pd # type: ignore
from matplotlib.ticker import ScalarFormatter, FuncFormatter  # Importando FuncFormatter
import os




PRINT_TO_FILE = True    # salva os graficos em arquivos pdf
PRINT_VALORES_MS=False  # reg para printar valores do termo ms no grafico


# identifica o OS e escolhe pasta
if os.name == 'nt': # windows
    SYSTEM=0
elif os.name == 'posix': # linux
    SYSTEM=1

if PRINT_TO_FILE:
    if SYSTEM:
        imageFolder="/home/ederson/Desktop/artigoSURVEY/" # pasta de imagens
        figg1="dopplerCurves.pdf" # nome de imagens
        #arquivoCSV=imageFolder+'valores.csv' # valores de pico da FFT normalizados para fazer a comparacao
        #arquivoCSV2=imageFolder+'valoresDopplerModeloCompleto.csv'
    else:
        imageFolder=r"C:/Users/eders/OneDrive/Área de Trabalho/artigoSURVEY/" # pasta de imagens windows
        figg1="dopplerCurves.pdf" # nome de imagens
        #arquivoCSV=imageFolder+'valores.csv' # valores de pico da FFT normalizados para fazer a comparacao
        #arquivoCSV2=imageFolder+'valoresDopplerModeloCompleto.csv'
            
DEBUG_PRINT=False
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
#plt.rcParams['text.usetex'] = True  # Ativa renderização com LaTeX


############################################## FUNCOES ####################

def calculateDeltaF(H,t):
    R = 6371000  # Raio da Terra em metros
    g = 9.80665  # Aceleração da gravidade em m/s^2
    c=299792458 # velocidade da luz no vacuo em m/s
    deltaF=1/(1+((1/c)*np.sqrt((g*R)/(1+H/R)))*(np.sin((np.sqrt(g / R) / (1 + H / R) ** (3 / 2)) * t)/np.sqrt((1+H/R)**2-2*(1+H/R)*np.cos((np.sqrt(g / R) / (1 + H / R) ** (3 / 2)) * t)+1)))-1
    return deltaF

def calculateF(H,t,F0):
    R = 6371000  # Raio da Terra em metros
    g = 9.80665  # Aceleração da gravidade em m/s^2
    c=299792458 # velocidade da luz no vacuo em m/s
    F=1/(1+((1/c)*np.sqrt((g*R)/(1+H/R)))*(np.sin((np.sqrt(g / R) / (1 + H / R) ** (3 / 2)) * t)/np.sqrt((1+H/R)**2-2*(1+H/R)*np.cos((np.sqrt(g / R) / (1 + H / R) ** (3 / 2)) * t)+1)))*F0
    return F



def plotDeltaFppm(deltaFppm,t):
    mar=0.25
    fonte1=14
    maxPpm = np.max(deltaFppm)
    tMaxPpm = t[np.argmax(deltaFppm)]
    minPpm = np.min(deltaFppm)
    tMinPpm = t[np.argmin(deltaFppm)]
    plt.text(tMaxPpm, maxPpm+1, f' Max: {maxPpm:.2f}', horizontalalignment='left', verticalalignment='bottom',fontsize=fonte1)
    plt.text(tMinPpm-5, minPpm-4.4, f' Min: {minPpm:.2f}', horizontalalignment='right', verticalalignment='bottom',fontsize=fonte1)
    plt.plot(t, deltaFppm)
    #plt.xlabel("Time(s)")
    #plt.ylabel("Doppler Shift $\delta_F$ (ppm)")
    plt.xlabel("Tempo (s)",fontsize=fonte1+2)
    plt.ylabel("Doppler Estático $\delta_F$ (ppm)",fontsize=fonte1+2)
    plt.tick_params(axis='both', labelsize=fonte1)
    
    plt.xlim(np.min(t),np.max(t) )
    plt.ylim(minPpm+minPpm*mar,maxPpm+maxPpm*mar )
    plt.text(tMaxPpm-(tMaxPpm/1.5), maxPpm+maxPpm*(0.1*mar)-1, '$\delta_F$', fontsize=16, ha='right', va='center')
    plt.grid(True)
    plt.show()

def plotF(F,t):
    mar=0.01
    fonte3=14
    maxF = np.max(F)
    tMaxF = t[np.argmax(F)]
    minF = np.min(F)
    tMinF = t[np.argmin(F)]
    plt.text(tMaxF, maxF+800, f' Max: {maxF:.0f} Hz', horizontalalignment='left', verticalalignment='bottom',fontsize=fonte3)
    plt.text(tMinF-5, minF-1800, f' Min: {minF:.0f} Hz', horizontalalignment='right', verticalalignment='bottom',fontsize=fonte3)
    plt.plot(t, F)
    #plt.xlabel("Time(s)")
    #plt.ylabel("Frequency (Hz)")
    plt.xlabel("Tempo(s)",fontsize=fonte3+2)
    plt.ylabel("Doppler estático $f$ (Hz)",fontsize=fonte3+4)
    
    plt.xlim(np.min(t),np.max(t) )
    plt.ylim(minF-2700,maxF+2700 )
    F0=436900000
    delta=(F-F0)/F0
    deltaMin=np.min(delta)
    deltaFmin=F0-minF
    deltaFmax=maxF-F0
    print(f'DeltaFmin: {deltaFmin:.0f}')
    print(f'DeltaFmax: {deltaFmax:.0f}')
    plt.yticks(ticks=[minF,F0,maxF], labels=[f'fc-{deltaFmax:0.0f} Hz',f'fc={F0/1e6:0.1f} MHz',f'fc+{deltaFmax:0.0f} Hz'],fontsize=fonte3)
    plt.tick_params(axis='x', labelsize=fonte3)
    plt.text(-15,F0+deltaFmax/2,'$f$',horizontalalignment='center', verticalalignment='top',fontsize=fonte3+3)
    plt.grid(True)
    plt.show()
    
    
    
    print(f' ppm min{deltaMin*1e6:.2f}')

def plotF_Hz_sec(F_Hz_sec,t):
    mar=0.2
    fonte4=14
    maxF_Hz_sec = np.max(F_Hz_sec)
    tMaxF_Hz_sec = t[np.argmax(F_Hz_sec)]
    minF_Hz_sec = np.min(F_Hz_sec)
    tMinF_Hz_sec = t[np.argmin(F_Hz_sec)]
    #plt.text(tMaxF_Hz_sec, maxF_Hz_sec, f' Max: {maxF_Hz_sec:.2f}', horizontalalignment='left', verticalalignment='bottom')
    plt.text(tMinF_Hz_sec, minF_Hz_sec-18*mar, f' Min: {minF_Hz_sec:.2f}', horizontalalignment='center', verticalalignment='top',fontsize=fonte4)
    plt.plot(t, F_Hz_sec)
    #plt.xlabel("Time(s)")
    #plt.ylabel("Frequency (Hz/s)")
    plt.xlabel("Tempo (s)",fontsize=fonte4+2)
    #plt.ylabel("Frequência (Hz/s)",fontsize=fonte4+2)
    plt.ylabel("Doppler dinâmico $\dot{f} \ (Hz/s)$",fontsize=fonte4+3)
    plt.xlim(np.min(t),np.max(t) )
    #plt.ylim(minF_Hz_sec+minF_Hz_sec*mar,maxF_Hz_sec+mar)
    plt.ylim(minF_Hz_sec-20,maxF_Hz_sec+20)
    plt.grid(True)
    plt.tick_params(axis='both', labelsize=fonte4)
    plt.yticks(np.arange(-160,41,40))
    plt.text(-80,-20,'$\dot{f}$',horizontalalignment='center', verticalalignment='top',fontsize=fonte4+3)
    #plt.title(rf'$\dot{{D_R}}$')
    plt.show()


def plotDeltaFppmSec(deltaFppmSec,t):
    mar=0.2
    maxPpmSec = np.max(deltaFppmSec)
    tMaxPpmSec = t[np.argmax(deltaFppmSec)]
    minPpmSec = np.min(deltaFppmSec)
    tMinPpmSec = t[np.argmin(deltaFppmSec)]
    plt.text(tMinPpmSec, minPpmSec, f'{minPpmSec:.2f}', horizontalalignment='center', verticalalignment='top')
    plt.plot(t, deltaFppmSec)
    plt.xlabel("Time(s)")
    plt.ylabel("Rate of change of Doppler shift ${\delta_F}'$ (ppm/s)")
    plt.xlim(np.min(t),np.max(t) )
    plt.ylim(minPpmSec+minPpmSec*mar,maxPpmSec+mar )
    plt.grid(True)
    plt.show()

def plotDeltaFppmAndSec(deltaFppm,deltaFppmSec,t):
    #fig, ax1 = plt.subplots() # Criando uma nova figura
    mar=0.25
    maxPpm = np.max(deltaFppm)
    tMaxPpm = t[np.argmax(deltaFppm)]
    minPpm = np.min(deltaFppm)
    tMinPpm = t[np.argmin(deltaFppm)]
    ax1.text(tMaxPpm, maxPpm+0.5, f' Max: {maxPpm:.2f}', horizontalalignment='left', verticalalignment='bottom',fontsize=ftext)
    ax1.text(tMinPpm-10, minPpm-5.5, f' Min: {minPpm:.2f}', horizontalalignment='right', verticalalignment='bottom',fontsize=ftext)
    ax1.set_xlim(np.min(t),np.max(t) )
    ax1.set_ylim(minPpm+minPpm*mar,maxPpm+maxPpm*mar )
    # Plotando deltaFppm no primeiro eixo y
    #color = 'tab:blue'
    #color = 'darkblue'
    color='black'
    #ax1.set_xlabel('Time (s)')
    #ax1.set_xlabel('Tempo (s)',fontsize=fonte2)
    ax1.set_xlabel('Time (s)',fontsize=flabels)
    #ax1.set_ylabel('Doppler Shift $\delta_F$ (ppm)', color=color)
    #ax1.set_ylabel('Doppler estático $\delta_F$ (ppm)', color=color,fontsize=fonte2+2)
    ax1.set_ylabel('Static Doppler $\delta_F$ [ppm]', color=color,fontsize=flabels)
    ax1.plot(t, deltaFppm, color=color)
    ax1.tick_params(axis='y', labelcolor=color,labelsize=fticks)
    ax1.text(tMaxPpm-(tMaxPpm/1.5), maxPpm+maxPpm*(0.1*mar)-1, '$\delta_F$', fontsize=ftext2, ha='right', va='center')
    # Criando o segundo eixo y
    ax2 = ax1.twinx()  
    maxPpmSec = np.max(deltaFppmSec)
    tMaxPpmSec = t[np.argmax(deltaFppmSec)]
    minPpmSec = np.min(deltaFppmSec)
    tMinPpmSec = t[np.argmin(deltaFppmSec)]
    
    
    #color = 'tab:red'
    color='darkgreen'
    #ax2.set_ylabel("Rate of change of Doppler shift ${\delta_F}'$ (ppm/s)", color=color)
    #ax2.set_ylabel("Doppler dinâmico ${\delta_F}'$ (ppm/s)", color=color, fontsize=fonte2+2)
    ax2.set_ylabel("Doppler rate ${\delta_F}'$ [ppm/s]", color=color, fontsize=flabels)
    ax2.plot(t, deltaFppmSec, color=color,linestyle='-.')
    
    ax2.tick_params(axis='y', labelcolor=color, labelsize=fticks)
    ax1.tick_params(axis='x', labelsize=fticks)

    
    
    ax2.text(tMinPpmSec -40, minPpmSec -0.05, f'Min: {minPpmSec:.2f}', horizontalalignment='center', verticalalignment='top',fontsize=ftext)
    ax2.set_ylim((minPpm+minPpm*mar)/20,(maxPpm+maxPpm*mar)/20)
    ax2.text(tMinPpm-(tMinPpm/3), maxPpmSec-minPpmSec*0.1+0.09, "${\delta_F}'$", fontsize=ftext2, ha='right', va='center')


    #print(tMaxPpm)
    ax1.grid(True)
    

def calculatesVelocity(H):
    R = 6371000  # Raio da Terra em metros
    g = 9.80665  # Aceleração da gravidade em m/s^2
    v = np.sqrt(g*R/(1+H/R))
    return v

######################  MAIN  ##################################
figFacecolor='#FFFFFF'
dpiSet=600
figWidth=3.5 #inches
figHeight=2.2  #inches
fticks=10 #tam fonte ticks
fleg=6.5#tam fonte leg
flabels=12#tam fonte titulos eixos
lwLeg=1.5 # expessura das linhas da legenda
ftext=9 # tam fonte texto
ftext2=11 # tam fonte texto
#fig, ax1 = plt.subplots() # Criando uma nova figura

#fig=plt.figure(figsize=(figWidth, figHeight),dpi=dpiSet,facecolor=figFacecolor) 

fig, ax1 = plt.subplots(figsize=(figWidth, figHeight), dpi=dpiSet, facecolor=figFacecolor)

    
# Calcula o Doppler Shift para H=200km e t[-150,150]
t = np.arange(-300, 301)  # Array de tempo de -150 a 150 segundos
npoints=100000
t = np.linspace(-300, 300, npoints)
#SAT1
H = 500000  # Altura em metros
deltaF=calculateDeltaF(H,t) # calcula deltaF
deltaFppm=deltaF*1e6 # calcular deltaF ppm
# calcula o Doppler dinamico
deltaF_ppm_per_sec = np.gradient(deltaFppm) / np.gradient(t)
deltaFppmSec = np.gradient(deltaFppm) / np.gradient(t)
#plotDeltaFppm(deltaFppm,t)
#plotDeltaFppmSec(deltaFppmSec,t)
plotDeltaFppmAndSec(deltaFppm,deltaFppmSec,t)
# #SAT2
# H = 200000  # Altura em metros
# deltaF=calculateDeltaF(H,t) # calcula deltaF
# deltaFppm=deltaF*1e6 # calcular deltaF ppm
# # calcula o Doppler dinamico
# deltaF_ppm_per_sec = np.gradient(deltaFppm) / np.gradient(t)
# deltaFppmSec = np.gradient(deltaFppm) / np.gradient(t)
# #plotDeltaFppm(deltaFppm,t)
# #plotDeltaFppmSec(deltaFppmSec,t)
# plotDeltaFppmAndSec(deltaFppm,deltaFppmSec,t)



if PRINT_TO_FILE:
    plt.savefig(imageFolder+figg1,bbox_inches='tight') #bbox_inches='tight'  evita cortes
    # Exibindo o gráfico
plt.show()

quit()

F=calculateF(H,t,436900000)
#plotF(F,t)
F_Hz_sec = np.gradient(F) / np.gradient(t)
F_Hz_sec_2 = np.gradient(F_Hz_sec) / np.gradient(t)
F_Hz_sec_3 = np.gradient(F_Hz_sec_2) / np.gradient(t)
#plotF_Hz_sec(F_Hz_sec,t)



######################
plt.figure()
print('Taxa de variacao do DR')
#plotF_Hz_sec(F_Hz_sec_2,t)


fo1=15
fo2=15
#############################
print('Taxa de variacao do DR denovo no intervalo')
plt.figure()
plt.plot(t,F_Hz_sec_2)
plt.xlabel('Tempo (s)', fontsize=fo1)
plt.ylabel(r'$ \ddot{D}(t)[Hz/s^2]$', fontsize=fo2)
plt.tick_params(axis='both', which='major', labelsize=14)
plt.grid()
minF2=np.min(F_Hz_sec_2)
maxF2=np.max(F_Hz_sec_2)
print(f'minimo = {minF2}')
print(f'maximo = {maxF2}')
# Encontrando os índices dos valores mínimo e máximo
index_minF2 = np.argmin(F_Hz_sec_2)
index_maxF2 = np.argmax(F_Hz_sec_2)
# Obtendo os valores de t correspondentes aos valores mínimo e máximo de F_Hz_sec_2
t_minF2 = t[index_minF2]
t_maxF2 = t[index_maxF2]
print(f'minimot = {t_minF2}')
print(f'maximot = {t_maxF2}')
SF=12
B=125e3
Ts=1/B
T=(2**SF)/B 
nsymbols=100
ToA=T*nsymbols
#t2min=-ToA/2
#t2max=ToA/2
t2min=0
t2max=ToA
# Criar o vetor t2 dentro do intervalo [t2min, t2max]
t2 = t[(t >= t2min) & (t <= t2max)]  # Filtrar t para o intervalo entre t2min e t2max
F2_t2 = F_Hz_sec_2[(t >= t2min) & (t <= t2max)]  # Correspondente aos valores de F2 para t2
F2_t2_min=np.min(F2_t2)
F2_t2_max=np.max(F2_t2)
plt.axhline(y=F2_t2_min, color='black', linestyle=':', linewidth=1)  # Linha pontilhada em y=0
plt.axhline(y=F2_t2_max, color='blue', linestyle=':', linewidth=1)  # Linha pontilhada em y=-4.596
# Plotando o novo gráfico com t2 sobreposto ao original, com uma cor diferente
plt.plot(t2, F2_t2, marker="o",color="red",label=f'Pacote LoRa  $n_S={nsymbols}$')
yticz=[minF2,maxF2,F2_t2_min,F2_t2_max]
# Adicionando os ticks no eixo y para F2_t2_min e F2_t2_max
ax = plt.gca()  # Obtendo os eixos do gráfico
#current_ticks_y = ax.get_yticks()  # Obtendo os ticks atuais do eixo y
#new_ticks_y = np.append(current_ticks_y, [F2_t2_min, F2_t2_max])  # Adicionando F2_t2_min e F2_t2_max aos ticks
#ax.set_yticks(new_ticks_y)  # Atualizando os ticks do eixo y
ax.set_yticks(yticz)  # Atualizando os ticks do eixo y
#########################################
plt.figure()
print('novo grafico doppler din')
plt.plot(t,F_Hz_sec)
#t2min=-ToA/2
#t2max=ToA/2
t2min=0
t2max=ToA
# Criar o vetor t2 dentro do intervalo [t2min, t2max]
t2 = t[(t >= t2min) & (t <= t2max)]  # Filtrar t para o intervalo entre t2min e t2max
F1_t2 = F_Hz_sec[(t >= t2min) & (t <= t2max)]  # Correspondente aos valores de F1 para t2
F1_t2_min=np.min(F1_t2)
F1_t2_max=np.max(F1_t2)
minF1=np.min(F_Hz_sec)
maxF1=np.max(F_Hz_sec)
#plt.axhline(y=F1_t2_min, color='black', linestyle=':', linewidth=1)  # Linha pontilhada em y=0
#plt.axhline(y=F1_t2_max, color='blue', linestyle=':', linewidth=1)  # Linha pontilhada em y=-4.596

# Plotando o novo gráfico com t2 sobreposto ao original, com uma cor diferente
plt.plot(t2, F1_t2, marker="o",color="red",label=f'Pacote LoRa  $n_S={nsymbols}$')
#plt.title('GRAFICO Y')
ytz=[minF1,maxF1,F1_t2_min,F1_t2_max]
ax = plt.gca()  # Obtendo os eixos do gráfico
#current_ticks_y = ax.get_yticks()  # Obtendo os ticks atuais do eixo y
#new_ticks_y = np.append(current_ticks_y, [F2_t2_min, F2_t2_max])  # Adicionando F2_t2_min e F2_t2_max aos ticks
#ax.set_yticks(new_ticks_y)  # Atualizando os ticks do eixo y
plt.grid()
plt.xlabel('Tempo (s)', fontsize=fo1)
plt.ylabel(r'$ \dot{D}(t)[Hz/s]$', fontsize=fo2)
plt.tick_params(axis='both', which='major', labelsize=14)
#comentei
#ax.set_yticks(ytz)  # Atualizando os ticks do eixo y
#ax.set_ylim(F1_t2_min-10,F1_t2_max+10)  # Atualizando os ticks do eixo y
# ate aqui
# Função para formatar os ticks do eixo y com 3 casas decimais
#formatter = FuncFormatter(lambda x, pos: f'{x:.3f}')
formatter = FuncFormatter(lambda x, pos: f'{x:.0f}')

ax.yaxis.set_major_formatter(formatter)


##################################################
#########################################
plt.figure()
print('novo grafico doppler din')
plt.plot(t,F_Hz_sec)
plt.title('GRAFICO X')
#t2min=-ToA/2
#t2max=ToA/2
t2min=0
t2max=ToA
# Criar o vetor t2 dentro do intervalo [t2min, t2max]
t2 = t[(t >= t2min) & (t <= t2max)]  # Filtrar t para o intervalo entre t2min e t2max
F1_t2 = F_Hz_sec[(t >= t2min) & (t <= t2max)]  # Correspondente aos valores de F1 para t2
F1_t2_min=np.min(F1_t2)
F1_t2_max=np.max(F1_t2)
minF1=np.min(F_Hz_sec)
maxF1=np.max(F_Hz_sec)
plt.axhline(y=F1_t2_min, color='black', linestyle=':', linewidth=1)  # Linha pontilhada em y=0
plt.axhline(y=F1_t2_max, color='blue', linestyle=':', linewidth=1)  # Linha pontilhada em y=-4.596
# Plotando o novo gráfico com t2 sobreposto ao original, com uma cor diferente
plt.plot(t2, F1_t2, marker="o",color="red",label=f'Pacote LoRa  $n_S={nsymbols}$')
plt.title('GRAFICO J')
ytz=[minF1,maxF1,F1_t2_min,F1_t2_max]
ax = plt.gca()  # Obtendo os eixos do gráfico
#current_ticks_y = ax.get_yticks()  # Obtendo os ticks atuais do eixo y
#new_ticks_y = np.append(current_ticks_y, [F2_t2_min, F2_t2_max])  # Adicionando F2_t2_min e F2_t2_max aos ticks
#ax.set_yticks(new_ticks_y)  # Atualizando os ticks do eixo y
ax.set_yticks(ytz)  # Atualizando os ticks do eixo y
ax.set_ylim(F1_t2_min-10,F1_t2_max+10)  # Atualizando os ticks do eixo y

# Função para formatar os ticks do eixo y com 3 casas decimais
formatter = FuncFormatter(lambda x, pos: f'{x:.3f}')
ax.yaxis.set_major_formatter(formatter)
ax.set_ylim([-142,-135])
ax.set_xlim([-20,20])

###################

plt.figure()
plt.plot(t,F_Hz_sec_3)

#ax=plt.gca()
#ax.set_xlim(-4,4)
### Exemplo SF=12 B=125kHz






Vel=calculatesVelocity(H)
print(f'Velocidade do SAT={Vel:.0f} m/s')
print(f'Velocidade do SAT={Vel/1000:.1f} km/s')
## exemplo de calculo de deltaF para pontos especificos
#pontos = np.array([-100, -25, 25, 100])
#deltaFpontos=calculateDeltaF(H,pontos)
#deltaFpontosPpm=deltaFpontos*1e6
#plotDeltaFppm(deltaFppm,t)
#plt.text(-25, 15, '$\delta_F$', fontsize=12, ha='right', va='center')
#plt.plot(t, deltaFppm)
#plt.scatter(pontos, deltaFpontosPpm, color='red', label='Pontos adicionais',s=20)
#plt.xlabel("Time(s)")
#plt.ylabel("Doppler Shift $\delta_F$ (ppm)")
#plt.xlim(-150, 150)
#plt.ylim(-30, 30)
#plt.grid(True)
#plt.show()
