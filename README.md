### Identificação do Candidato

- **Nome completo: Rennan Oliveira**
- **GitHub: RennanOS**

---

## Visão Geral da Solução

Este projeto implementa um contador de produção não-intrusivo utilizando um ESP32 e um sensor óptico baseado em LDR. O objetivo é monitorar automaticamente a passagem de peças em uma esteira, eliminando a necessidade de contagem manual e permitindo o acompanhamento da produção em tempo real.

O sistema identifica a passagem de uma peça pela variação da luminosidade detectada pelo sensor. Além da contagem, também monitora o tempo em que o sensor permanece bloqueado para identificar possíveis micro-paradas na linha de produção. Um botão físico permite reiniciar o turno, zerando os contadores e variáveis de monitoramento.

Toda a interação do usuário ocorre por meio do monitor serial, onde são exibidas as mensagens de inicialização, contagem de peças, detecção de micro-paradas e confirmação do reset.

---

## Arquitetura do Sistema Embarcado

O programa foi desenvolvido utilizando um laço principal (while True) responsável por monitorar continuamente o sensor óptico e o botão de reset.

A lógica do sistema é baseada em estados:

- Linha livre: sensor detecta iluminação normal.
- Linha bloqueada: uma peça interrompe o feixe de luz.
- Contagem: a peça é contabilizada apenas quando o sensor retorna ao estado de iluminação normal (borda de subida), evitando múltiplas contagens da mesma peça.
- Micro-parada: caso o sensor permaneça bloqueado por mais de 5 segundos, é emitido um alerta no monitor serial.
- Reset: ao detectar o acionamento do botão, o contador e as variáveis de controle são reinicializados.

Fluxo simplificado:

Inicialização <br>
      │<br>
      ▼<br>
Leitura contínua do LDR<br>
      │<br>
      ├── Sensor bloqueado?<br>
      │        <br> │<br>
      │        <br> ├── Sim → inicia temporização<br>
      │        <br> │<br>
      │        <br> └── Mantido por 5 s → alerta de micro-parada<br>
      │<br>
      ├── Sensor voltou ao normal?<br>
      │        <br> │<br>
      │        <br> └── Incrementa contador<br>
      │<br>
      └── Botão pressionado?<br>
               <br> │<br>
               <br> └── Reinicia contadores<br>

---

## Componentes Utilizados na Simulação

- ESP32 DevKit C v4
  - Responsável pelo processamento da aplicação e execução do firmware.
- Sensor Óptico (Photoresistor/LDR)
  - Detecta a variação da luminosidade provocada pela passagem das peças na esteira.
- Botão Push Button
  - Permite realizar o reset manual do turno de produção.
- Monitor Serial
  - Exibe todas as mensagens de operação e monitoramento do sistema.

---

## Decisões Técnicas Relevantes

Durante o desenvolvimento foram adotadas algumas decisões para tornar o sistema mais confiável e compatível com os testes automatizados:

- Utilização de uma máquina de estados simples para evitar múltiplas contagens da mesma peça.
- A contagem é realizada somente quando a iluminação retorna ao estado normal, garantindo que a peça tenha passado completamente pelo sensor.
- A detecção de micro-paradas utiliza temporização não bloqueante com time.ticks_ms(), permitindo que o sistema continue executando todas as demais tarefas simultaneamente.
- Os valores de referência do sensor foram definidos a partir das leituras observadas durante a simulação no Wokwi, utilizando diretamente os valores do ADC para aumentar a precisão da detecção.
- As mensagens enviadas pela interface serial seguem exatamente o padrão especificado no enunciado para garantir compatibilidade com os testes automatizados.

---

## Resultados Obtidos

O sistema desenvolvido atende aos requisitos propostos no desafio.

Durante a simulação foi possível verificar:

- Inicialização correta do sistema.
- Contagem automática das peças ao detectar a passagem pelo sensor.
- Detecção de micro-paradas quando o sensor permanece bloqueado por mais de cinco segundos.
- Reset correto dos contadores através do botão físico.
- Exibição das mensagens esperadas no monitor serial.

Todos os cenários de teste automatizados disponibilizados para o projeto foram executados com sucesso.

---

## Comentários Adicionais (Opcional)

Durante o desenvolvimento, a principal dificuldade foi compreender o comportamento do sensor óptico utilizado na simulação. Foi necessário realizar testes para identificar a relação entre os valores de luminosidade configurados no Wokwi e os valores efetivamente retornados pelo conversor analógico-digital (ADC), permitindo definir limiares adequados para a detecção da passagem das peças.

Outro ponto observado foi o comportamento da simulação em relação ao uso de pequenas pausas (time.sleep_ms()), que precisaram ser removidas para garantir compatibilidade com os testes automatizados.

Como melhoria futura, o sistema poderia incluir um display para visualização local da produção, armazenamento histórico das medições e comunicação via Wi-Fi ou MQTT para envio dos dados a uma plataforma de monitoramento remoto.

O desenvolvimento do projeto permitiu reforçar conceitos de sistemas embarcados, leitura de sensores analógicos, programação orientada a eventos, utilização de temporização não bloqueante e validação de firmware por meio de testes automatizados.
