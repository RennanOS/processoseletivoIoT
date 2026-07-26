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

# Ajuste nos limiares para o Wokwi
ADC_LIVRE = 1200       # Valor abaixo disso = livre (claro)
ADC_BLOQUEADO = 2000   # Valor acima disso = bloqueado (escuro)

MICRO_PARADA_MS = 5000
DEBOUNCE_MS = 50

# =====================================================
# Variáveis
# =====================================================

contador = 0
linha_bloqueada = False
inicio_bloqueio = 0
micro_parada_detectada = False

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
    
    # Fim da passagem da peça (libertação)
    elif linha_bloqueada and adc < ADC_LIVRE:
        linha_bloqueada = False
        contador += 1
        print(f"Peca detectada! Total: {contador}")
    
    # -------------------------------------------------
    # Micro-parada (5 segundos bloqueado)
    # -------------------------------------------------
    
    if linha_bloqueada and not micro_parada_detectada:
        if time.ticks_diff(agora, inicio_bloqueio) >= MICRO_PARADA_MS:
            print("Alerta: Micro-parada detectada!")
            micro_parada_detectada = True
    
    # -------------------------------------------------
    # Botão de Reset (com debounce)
    # -------------------------------------------------
    
    if botao.value() == 0:  # Botão pressionado (Pull-Up)
        time.sleep_ms(DEBOUNCE_MS)  # Debounce
        
        if botao.value() == 0:  # Confirma pressionamento
            resetar_turno()
            
            # Aguarda soltar o botão
            while botao.value() == 0:
                time.sleep_ms(10)
    
    # Pequeno delay para não sobrecarregar
    time.sleep_ms(10)