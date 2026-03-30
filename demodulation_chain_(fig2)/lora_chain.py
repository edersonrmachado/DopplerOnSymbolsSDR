"""
lora_chain.py

Description:
    Modulates and demodulates a LoRa symbol producing graphic outputs.

Use:
    python lora_chain.py 

Autor:
    Ederson Ribas Machado

Date:
    2026-03-29
"""

# imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft

# entries (replace by your folder)
image_folder="/home/ederson/Desktop/figures/" # linux
#image_folder=r"C:\Users\Desktop\figures\\" # windows

# fig names
figg1='fig1.svg'
figg2='fig2.svg'
figg3='fig3.svg'
figg4='fig4.svg'
        
# options
DEBUG_PRINT=False # print debug additional information 
PLOT_LEGEND=False  # print legend for one figure
SAVE_AND_SHOW_PLOTS=True    
LATEX_FONT_LABELS=False

plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
#plt.rcParams['text.usetex'] = True  # Ativa renderização com LaTeX


###### Gera simbolo com fs arbitrario 

def symbolGen(s,SF,B,fs): 
    N=2**SF
    Ts=1/fs
    T=(2**SF)/B
    ## ajuste do numero de amostras e limites
    #nAmostras=int(fs*T)
    nAmostras=int(N*fs/B)
    
    intervalN=np.arange(0,nAmostras)
    #nlim=int((T/Ts)*(1-s/N))
    nlim=int((N-s)*(fs/B))
    
    ## Aplica a funcao de geração de símbolo
    xn=[]
    fn=[]
    for n in intervalN:
        if 0<=n<nlim:
            x=np.exp(2*np.pi*1j*(((B*Ts*n)**2)/(2*N)+(s/N-1/2)*n*Ts*B)) 
            f_i = (n * B**2) / (N * fs**2) + (s * B) / (N * fs) - (B / (2 * fs))
            #print(f'I1={n}')
        elif nlim<=n<nAmostras:
            x=np.exp(2*np.pi*1j*(((B*Ts*n)**2)/(2*N)+(s/N-3/2)*n*Ts*B))
            f_i = (n * B**2) / (N * fs**2) + (s * B) / (N * fs) - (3 * B) / (2 * fs)
           # print(f'I2={n}')
        xn.append(x)
        fn.append(f_i) 
    return xn

###### Calcula frequencia instantanea normalizada e em rad/amostra

def calcula_argumento(in_vector,mode):
# mode 0 metodo com N amostras
# metodo com N-1 amostras desloca arg[0]
    if mode: # mode 1 igual ao equacionamento
        comp=[0] * (len(in_vector))
        arg=[0] * (len(in_vector))
        for n in range(len(in_vector)):
            #print(n)
            comp[n]=in_vector[n]*np.conj(in_vector[n-1])     
            arg[n]=np.angle(comp[n])
    else: #mode 0 desloca uma unidade
        comp=[0] * (len(in_vector) - 1)
        arg=[0] * (len(in_vector) - 1)
        for n in range(len(in_vector)-1):
            comp[n]=in_vector[n+1]*np.conj(in_vector[n])     
            arg[n]=np.angle(comp[n])
    return np.array(arg)

def calcula_argumento2(in_vector):
    comp=[0] * (len(in_vector))
    arg=[0] * (len(in_vector))
    for n in range(len(in_vector)):
        arg[n]=(np.angle(in_vector[n])-np.angle(in_vector[n-1]))%(2*np.pi)
    return np.array(arg)
    #return (compa)
    '''
    for n in range(len(in_vector)-1):
        arg[n]=np.angle(in_vector[n])
        comp[n]=(arg[n+1]- arg[n])  % 2*np.pi   
    return np.array(comp)       
    '''
####### calcula freq instantanea em Hz/amostra
def fi_norm(x,fs,B):
    return (x*(fs/B))/(2*np.pi)

#######  gera ruido
def generate_AWGN(vector,SNR):
    magnitude = np.abs(vector) # calcula modulo das amostras do sinal complexo   
    power_inst_vector= magnitude**2 # calcula a potencia instantanea das amostras c
    power_mean=np.mean(power_inst_vector) # calcula a potencia media do intervalo amostral (w)
    power_mean_db = 10 * np.log10(power_mean) # calcula a media 
    noise_mean_db=power_mean_db-SNR # calcula a media em db do ruido desejado
    noise_mean=10**(noise_mean_db/10) # calcula media linear (watts) do ruido desejado
    #mu,sigma = 0, noise_mean/2
    #noise_real=np.random.normal(mu,sigma,len(vector))
    #noise_imag=np.random.normal(mu,sigma,len(vector))
    #noise_complex = noise_real + 1j * noise_imag
    mu,sigma = 0, np.sqrt(noise_mean)# desvio padrao eh a raiz da variancia 
    noise_real=np.random.normal(mu,sigma,len(vector))/np.sqrt(2)
    noise_imag=np.random.normal(mu,sigma,len(vector))/np.sqrt(2)
    noise_complex = noise_real + 1j * noise_imag
    
    magnitude_noise=np.abs(noise_complex)
    power_inst_noise=magnitude_noise**2
    power_mean_noise=np.mean(power_inst_noise)
    power_mean_noise_db=10 * np.log10(power_mean_noise) 
    
        
    if DEBUG_PRINT:
        print("VALORES TEORICOS")
        print(f"pot media do sinal={power_mean:.6f}")
        print(f"Pot media do sinal em db={power_mean_db:.6f}")
        print(f"Pot media do ruido em db={noise_mean_db:.6f}")
        print(f"Pot media do ruido={noise_mean:.6f}")
        print("VALORES PRATICOS")
        print(f"pot media do ruido={power_mean_noise:.6f}")
        print(f"Pot media do ruido em db={power_mean_noise_db:.6f}")
        print()
        
    return noise_complex
#############################################################################
## main
SF=7 #define o SF
s=10 #define o simbolo
B=125e3 # define B
fs=B    # define fs
SNR=20  # define o SNR
mode=0 # modo para calcular freq
xn=symbolGen(s,SF,B,fs)# gera simbolo s 
arg=calcula_argumento(xn,mode) # calcula argumento
freq_normal=fi_norm(arg,fs,B) # calcula freq
x0=symbolGen(0,SF,B,fs) # gera o simbolo zero
x0conj=np.conj(x0) #gera simbolo de referencia que eh o conjugado do simbolo 0
argX0conj=calcula_argumento(x0conj,mode) # calcula argumento antes da freq
freq_normalx0conj=fi_norm(argX0conj,fs,B) # calcula freq
r=generate_AWGN(xn,SNR) # gera vetor de ruido
y=(xn+r) # soma o ruido 
#y=(xn) # soma o ruido 
#print('SEM RUIDO')
argy=calcula_argumento(y,mode) # calcula argumento do sinal com ruido
freq_normaly=fi_norm(argy,fs,B) # calcula freq do sinal com ruido
dec=y*x0conj # faz o dechirping
#argDec=calcula_argumento(dec,mode)
argDec=calcula_argumento2(dec)
freq_normalDec=fi_norm(argDec,fs,B)
#freq_normalDec=calcula_argumento2(dec)
#freq_normalDec=argDec
#print("aaaaaaa",freq_normalDec)


#print(dec)
mult=np.array(fft(dec)) # faz a fft
estimated_symbol = np.argmax(np.abs(mult)) # estima o símbolo 

indices_picos = np.argpartition(mult, -2)[-2:]  # Obtém os índices dos dois maiores valores
indices_picos = indices_picos[np.argsort(mult[indices_picos])[::-1]]  # Ordena em ordem decrescente
#   print(f's={s}, estimated={estimated_symbol}')
#x1=np.array(xn)
#energia = np.sum(np.abs(x1)**2)
#print(f'Energia={energia}')
T=(2**SF)/B
N=2**SF
## ajuste do numero de amostras e limites
#nAmostras=int(fs*T)
nAmostras=int(N*fs/B)
fontTitle=20
fsize1=20
fsize2=14
lwid=2
ffont=20
fzin=16
fz=14
faa=15

figWidth=3.5
figHeight=6.2
figFacecolor="#F7F7F7"
fonteTickX=23
lwidPLots=3.5
larguraBorda=1.5
padXlabel=-20
padYlabel=10
fonteXlabel=25
fonteYlabel=26
Msize=7.5
fonteYticks=24
espacoVerticalEntrePlots=0.34
fonteYticksB=28
padYlabelFFT=3
fonteLegenda=25

############################## figura  1
fig1=plt.figure(figsize=(figWidth, figHeight),dpi=300,facecolor=figFacecolor) 
##########################
##############  freq x[n]
ax = fig1.add_subplot(2, 1, 1)
ax.set_yticks([-0.5,  0.5])
ax.set_yticklabels(['-'+r'$\frac{B}{2}$',r'$\frac{B}{2}$'],fontsize=fonteYticksB)
ax.set_xticks([0,nAmostras-1])
ax.set_xticklabels([0,nAmostras-1],fontsize=fonteTickX)

ax.set_ylabel('Frequency',fontsize=fonteYlabel,labelpad=padYlabel)
ax.set_xlabel('n samples',labelpad=padXlabel,fontsize=fonteXlabel)

if LATEX_FONT_LABELS:
    ax.set_ylabel(r'\textit{Frequency}',fontsize=fonteYlabel,labelpad=padYlabel)
    ax.set_xlabel(r'\textit{n samples}',labelpad=padXlabel,fontsize=fonteXlabel)


ax.plot(freq_normal, marker='o',markersize=Msize)
for spine in ax.spines.values():
    spine.set_linewidth(larguraBorda)  # ou qualquer valor desejado
##############
ax = fig1.add_subplot(2, 1, 2)
ax.set_yticks([-1, 1])  
ax.set_yticklabels([-1,1],fontsize=fonteTickX)
ax.set_xticks([0,nAmostras-1])
ax.set_xticklabels([0,nAmostras-1],fontsize=fonteTickX)

ax.set_xlabel('n samples',labelpad=padXlabel,fontsize=fonteXlabel)
ax.set_ylabel('Amplitude',fontsize=fonteYlabel,labelpad=padYlabel)
ax.plot(np.real(xn),label='Real',lw=lwidPLots)
ax.plot(np.imag(xn),label='Imag.',color="lightcoral",lw=lwidPLots)#,linestyle=':')

if LATEX_FONT_LABELS:
    ax.set_xlabel(r'\textit{n samples}',labelpad=padXlabel,fontsize=fonteXlabel)
    ax.set_ylabel(r'\textit{Amplitude}',fontsize=fonteYlabel,labelpad=padYlabel)
    ax.plot(np.real(xn),label=r'\textit{Real}',lw=lwidPLots)
    ax.plot(np.imag(xn),label=r'\textit{Imag.}',color="lightcoral",lw=lwidPLots)#,linestyle=':')

for spine in ax.spines.values():
    spine.set_linewidth(larguraBorda)  # ou qualquer valor desejado
fig1.subplots_adjust(hspace=espacoVerticalEntrePlots)
############## legenda
if PLOT_LEGEND:
    ax.legend(loc=1,frameon=True,fancybox=True,bbox_to_anchor=(-0.3, 1.45),fontsize=fonteLegenda, shadow=True,handlelength=0.9,edgecolor='black',handletextpad=0.2,facecolor=figFacecolor)
############## salva Grafico
if SAVE_AND_SHOW_PLOTS:
    plt.savefig(image_folder+figg1,bbox_inches='tight') #bbox_inches='tight'  evita cortes
#############

############################## figura  1
fig2=plt.figure(figsize=(figWidth, figHeight),dpi=300,facecolor=figFacecolor) 
##########################
##############  freq x[n]
ax = fig2.add_subplot(2, 1, 1)
ax.set_yticks([-0.5,  0.5])
ax.set_xticks([0,nAmostras-1])
ax.set_xticklabels([0,nAmostras-1],fontsize=fonteTickX)

ax.set_yticklabels(['-'+r'$\frac{B}{2}$',r'$\frac{B}{2}$'],fontsize=fonteYticksB)
ax.set_xlabel('n samples',labelpad=padXlabel,fontsize=fonteXlabel)

if LATEX_FONT_LABELS:
    ax.set_xlabel(r'\textit{n samples}',labelpad=padXlabel,fontsize=fonteXlabel)
ax.plot(freq_normaly, marker='o',markersize=Msize)
for spine in ax.spines.values():
    spine.set_linewidth(larguraBorda)  # ou qualquer valor desejado
##############
ax = fig2.add_subplot(2, 1, 2)
ax.set_yticks([-1, 1])  
ax.set_yticklabels([-1,1],fontsize=fonteTickX)
ax.set_xticks([0,nAmostras-1])
ax.set_xticklabels([0,nAmostras-1],fontsize=fonteTickX)
ax.set_xlabel('n samples',labelpad=padXlabel,fontsize=fonteXlabel)
ax.plot(np.real(y),label='Real',lw=lwidPLots)
ax.plot(np.imag(y),label='Imag.',color="lightcoral",lw=lwidPLots)#,linestyle=':')
if LATEX_FONT_LABELS:
    ax.set_xlabel(r'\textit{n samples}',labelpad=padXlabel,fontsize=fonteXlabel)
    ax.plot(np.real(y),label=r'\textit{Real}',lw=lwidPLots)
    ax.plot(np.imag(y),label=r'\textit{Imag.}',color="lightcoral",lw=lwidPLots)#,linestyle=':')
for spine in ax.spines.values():
    spine.set_linewidth(larguraBorda)  # ou qualquer valor desejado
fig2.subplots_adjust(hspace=espacoVerticalEntrePlots)
############## legenda
#ax.legend(loc=1,frameon=True,fancybox=True,bbox_to_anchor=(-0.07, 1.45),fontsize=fz, shadow=False,#handlelength=0.5,edgecolor='black',handletextpad=0.2)
############## salva Grafico
if SAVE_AND_SHOW_PLOTS:
    plt.savefig(image_folder+figg2,bbox_inches='tight') #bbox_inches='tight'  evita cortes
    plt.show()


############################## figura  1
fig3=plt.figure(figsize=(figWidth, figHeight),dpi=300,facecolor=figFacecolor) 
##########################
##############  freq x[n]
freq_normalDec = np.round(freq_normalDec, 6)
ax = fig3.add_subplot(2, 1, 1)
#ax.set_yticks([-0.5,  0.5])
ymin=-0.05
ymax=1.05
ax.set_ylim(ymin, ymax)
ax.set_yticks([0, 1])
ax.set_xticks([0,nAmostras-1])
ax.set_xticklabels([0,nAmostras-1],fontsize=fonteTickX)
ax.set_yticklabels(['0','B'],fontsize=fonteYticks)
ax.set_xlabel('n samples',labelpad=padXlabel,fontsize=fonteXlabel)
if LATEX_FONT_LABELS:
    ax.set_yticklabels([r'$0$',r'$B$'],fontsize=fonteYticks)
    ax.set_xlabel(r'\textit{n samples}',labelpad=padXlabel,fontsize=fonteXlabel)
ax.plot(freq_normalDec, marker='o',markersize=Msize)
for spine in ax.spines.values():
    spine.set_linewidth(larguraBorda)  # ou qualquer valor desejado
##############
ax = fig3.add_subplot(2, 1, 2)
ax.set_yticks([-1, 1])  
ax.set_yticklabels([-1,1],fontsize=fonteTickX)
ax.set_xticks([0,nAmostras-1])
ax.set_xticklabels([0,nAmostras-1],fontsize=fonteTickX)
ax.set_xlabel('n samples',labelpad=padXlabel,fontsize=fonteXlabel)
ax.plot(np.real(dec),label='Real',lw=lwidPLots)
ax.plot(np.imag(dec),label='Imag.',color="lightcoral",lw=lwidPLots)#,linestyle=':')
if LATEX_FONT_LABELS:
    ax.set_xlabel(r'\textit{n samples}',labelpad=padXlabel,fontsize=fonteXlabel)
    ax.plot(np.real(dec),label=r'\textit{Real}',lw=lwidPLots)
    ax.plot(np.imag(dec),label=r'\textit{Imag.}',color="lightcoral",lw=lwidPLots)#,linestyle=':')
for spine in ax.spines.values():
    spine.set_linewidth(larguraBorda)  # ou qualquer valor desejado
fig3.subplots_adjust(hspace=espacoVerticalEntrePlots)
############## legenda
#ax.legend(loc=1,frameon=True,fancybox=True,bbox_to_anchor=(-0.07, 1.45),fontsize=fz, shadow=False,#handlelength=0.5,edgecolor='black',handletextpad=0.2)
############## salva Grafico
if SAVE_AND_SHOW_PLOTS:
    plt.savefig(image_folder+figg3,bbox_inches='tight') #bbox_inches='tight'  evita cortes
    plt.show()

fig4=plt.figure(figsize=(figWidth, figHeight),dpi=300,facecolor=figFacecolor) 
##########################
##############  freq x[n]
ax = fig4.add_subplot(2, 1, 1)

ax.set_yticks([ 0, 2**SF])
ax.set_yticklabels([0,2**SF],fontsize=fonteYticks)
ax.plot(np.abs(mult), marker='o',markersize=Msize)
ax.set_xticks([0,nAmostras-1])
ax.set_xticklabels([0,nAmostras-1],fontsize=fonteTickX)

ax.set_xlabel('k bins',labelpad=padXlabel,fontsize=fonteXlabel)
ax.set_ylabel('Magnitude',labelpad=padYlabelFFT,fontsize=fonteYlabel)

if LATEX_FONT_LABELS:
    ax.set_xlabel(r'\textit{k bins}',labelpad=padXlabel,fontsize=fonteXlabel)
    ax.set_ylabel(r'\textit{Magnitude}',labelpad=padYlabelFFT,fontsize=fonteYlabel)
current_ticks = ax.get_xticks()
new_tick = estimated_symbol  # O valor do novo tick que você quer adicionar
new_ticks = np.append(current_ticks, estimated_symbol)
ax.set_xticks(new_ticks) # Atualizando os ticks no eixo x, sem remover os existentes
ax.set_xticks([0,estimated_symbol,nAmostras-1])
ax.set_xticklabels(['',estimated_symbol, nAmostras-1],fontsize=fonteTickX)
for spine in ax.spines.values():
    spine.set_linewidth(larguraBorda)  # ou qualquer valor desejado
##############
fig4.subplots_adjust(hspace=espacoVerticalEntrePlots)
############## legenda
#ax.legend(loc=1,frameon=True,fancybox=True,bbox_to_anchor=(-0.07, 1.45),fontsize=fonteLegenda, shadow=True,handlelength=0.5,edgecolor='black',handletextpad=0.2)
############## salva Grafico
if SAVE_AND_SHOW_PLOTS:
    plt.savefig(image_folder+figg4,bbox_inches='tight') #bbox_inches='tight'  evita cortes
    plt.show()

