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

ADC_LIVRE = 1200
ADC_BLOQUEADO = 2000

MICRO_PARADA_MS = 5000
DEBOUNCE_MS = 50

# =====================================================
# Variáveis
# =====================================================

contador = 0

linha_bloqueada = False

inicio_bloqueio = 0
micro_parada_detectada = False

ultimo_estado_botao = botao.value()
ultima_mudanca_botao = time.ticks_ms()
botao_processado = False

print("Contador de Producao Inicializado")

# =====================================================
# Loop Principal
# =====================================================

while True:

    agora = time.ticks_ms()

    # -------------------------------------------------
    # Leitura do sensor
    # -------------------------------------------------

    adc = ldr.read()

    # -------------------------------------------------
    # Peça entrou
    # -------------------------------------------------

    if (not linha_bloqueada) and (adc > ADC_BLOQUEADO):

        linha_bloqueada = True
        inicio_bloqueio = agora
        micro_parada_detectada = False

    # -------------------------------------------------
    # Peça saiu
    # -------------------------------------------------

    elif linha_bloqueada and (adc < ADC_LIVRE):

        linha_bloqueada = False

        contador += 1

        print(f"Peca detectada! Total: {contador}")

    # -------------------------------------------------
    # Micro-parada
    # -------------------------------------------------

    if linha_bloqueada:

        if (not micro_parada_detectada and
            time.ticks_diff(agora, inicio_bloqueio) >= MICRO_PARADA_MS):

            print("Alerta: Micro-parada detectada!")
            micro_parada_detectada = True

    # -------------------------------------------------
    # Debounce do botão
    # -------------------------------------------------

    estado = botao.value()

    if estado != ultimo_estado_botao:

        ultimo_estado_botao = estado
        ultima_mudanca_botao = agora

    if time.ticks_diff(agora, ultima_mudanca_botao) >= DEBOUNCE_MS:

        if estado == 0 and not botao_processado:

            contador = 0
            linha_bloqueada = False
            micro_parada_detectada = False
            inicio_bloqueio = 0

            print("Turno resetado com sucesso. Contadores zerados.")

            botao_processado = True

        elif estado == 1:

            botao_processado = False

    time.sleep_ms(10)