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

print("Contador de Producao Inicializado")

# =====================================================
# Loop Principal
# =====================================================

while True:

    agora = time.ticks_ms()

    # -------------------------------------------------
    # Sensor
    # -------------------------------------------------

    adc = ldr.read()

    # Início da passagem da peça
    if (not linha_bloqueada) and (adc > ADC_BLOQUEADO):

        linha_bloqueada = True
        inicio_bloqueio = agora
        micro_parada_detectada = False

    # Fim da passagem da peça
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
    # Botão (debounce + borda)
    # -------------------------------------------------

    estado = botao.value()

    if ultimo_estado_botao == 1 and estado == 0:

        contador = 0
        linha_bloqueada = False
        inicio_bloqueio = 0
        micro_parada_detectada = False

        print("Turno resetado com sucesso. Contadores zerados.")

        ultimo_estado_botao = estado

    time.sleep_ms(1)