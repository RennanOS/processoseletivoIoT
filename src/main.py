from machine import Pin, ADC
import time

# =====================================================
# Configuração de Hardware
# =====================================================

LDR_PIN = 34
BUTTON_PIN = 13

ldr = ADC(Pin(LDR_PIN))
ldr.atten(ADC.ATTN_11DB)

botao = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

# Valores ajustados para o Wokwi
ADC_LIVRE = 1500       
ADC_BLOQUEADO = 2500   

MICRO_PARADA_MS = 5000
DEBOUNCE_MS = 50

# =====================================================
# Variáveis
# =====================================================

contador = 0
linha_bloqueada = False
inicio_bloqueio = 0
micro_parada_detectada = False

# Estado do botão para debounce
ultimo_estado_botao = 1
ultimo_tempo_botao = 0

print("Contador de Producao Inicializado")

# =====================================================
# Funções
# =====================================================

def resetar_turno():
    global contador, linha_bloqueada, inicio_bloqueio, micro_parada_detectada
    contador = 0
    linha_bloqueada = False
    inicio_bloqueio = 0
    micro_parada_detectada = False
    print("Turno resetado com sucesso. Contadores zerados.")

# =====================================================
# Loop Principal
# =====================================================

while True:
    agora = time.ticks_ms()
    
    # -------------------------------------------------
    # Sensor LDR
    # -------------------------------------------------
    
    adc = ldr.read()
    
    # Início da passagem da peça (bloqueio)
    if not linha_bloqueada and adc > ADC_BLOQUEADO:
        linha_bloqueada = True
        inicio_bloqueio = agora
        micro_parada_detectada = False
    
    # Fim da passagem da peça (libertação) -> CONTA!
    elif linha_bloqueada and adc < ADC_LIVRE:
        linha_bloqueada = False
        contador += 1
        print(f"Peca detectada! Total: {contador}")
    
    # -------------------------------------------------
    # Micro-parada
    # -------------------------------------------------
    
    if linha_bloqueada and not micro_parada_detectada:
        if time.ticks_diff(agora, inicio_bloqueio) >= MICRO_PARADA_MS:
            print("Alerta: Micro-parada detectada!")
            micro_parada_detectada = True
    
    # -------------------------------------------------
    # Botão de Reset (com debounce)
    # -------------------------------------------------
    
    estado_atual = botao.value()
    
    # Detecta borda de descida (pressionou)
    if estado_atual == 0 and ultimo_estado_botao == 1:
        # Debounce
        time.sleep_ms(DEBOUNCE_MS)
        if botao.value() == 0:
            resetar_turno()
            # Aguarda soltar
            while botao.value() == 0:
                time.sleep_ms(10)
    
    ultimo_estado_botao = estado_atual
    
    # Delay para não sobrecarregar
    time.sleep_ms(50)