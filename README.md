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
      │         │<br>
      │         ├── Sim → inicia temporização<br>
      │         │<br>
      │         └── Mantido por 5 s → alerta de micro-parada<br>
      │<br>
      ├── Sensor voltou ao normal?<br>
      │         │<br>
      │         └── Incrementa contador<br>
      │<br>
      └── Botão pressionado?<br>
                │<br>
                └── Reinicia contadores<br>

---

## Componentes Utilizados na Simulação

Liste os principais componentes definidos no `diagram.json`, por exemplo:

- Tipo de placa utilizada
- LEDs, botões, sensores, atuadores, etc.
- Função de cada componente no sistema

---

## Decisões Técnicas Relevantes

Explique brevemente decisões importantes tomadas durante o desenvolvimento, como:

- Organização do código
- Uso de funções, estados ou constantes
- Estratégias para temporização ou controle lógico

---

## Resultados Obtidos

Descreva o comportamento final do sistema:

- O que funciona corretamente
- Quais requisitos foram atendidos
- Resultado observado na simulação do Wokwi

---

## Comentários Adicionais (Opcional)

Utilize este espaço para comentar, se desejar:

- Dificuldades encontradas
- Limitações da solução
- Melhorias que você faria com mais tempo
- Principais aprendizados durante o desafio

---

> Este relatório faz parte da avaliação técnica.  
> Clareza, objetividade e organização são tão importantes quanto o funcionamento do código.

---

## Especificação dos Testes Automatizados (Wokwi CI)

Para que o projeto seja validado com sucesso na esteira de integração contínua (CI), o firmware escrito em MicroPython deve interagir corretamente com as leituras dos sensores descritos em cada cenário e enviar as mensagens de status exatas.

### Requisitos Críticos de Implementação

1. **Casamento Exato de Strings:** O Wokwi CI faz uma verificação estrita caractere por caractere. Se houver divergência em maiúsculas/minúsculas, acentuação ou falta de pontuação, o teste irá falhar.
2. **Arquitetura Não-Bloqueante:** Evite o uso de funções bloqueantes. Elas podem fazer com que o firmware perca a janela de tempo em que o simulador altera o peso, quebrando a sincronia do teste automatizado.

---

## Suporte

Em caso de dúvidas:

- Consulte o material dos cursos EAD
- Leia atentamente este README
- Analise os logs das GitHub Actions
- Utilize os canais oficiais para contato com os instrutores
