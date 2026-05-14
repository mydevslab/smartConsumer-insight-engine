# Um pouco da Jornada do Esquadrão 12 no Hackathon Elas+ Tech

## 1. Visão Geral e Contexto do Hackathon

O Hackathon Elas+ Tech representou o ápice de um ciclo intensivo de seis meses de formação, desafiando as participantes a converterem densidade técnica em soluções de mercado em uma janela de alta performance (4 a 8 de maio). O Esquadrão 12 assumiu o desafio central: "Sistema inteligente de análise financeira e geração de insights", posicionando-se sob a ótica da **Tríplice Hélice da Inovação** (Universidade, Governo e Empresa) para garantir que o projeto não fosse apenas um exercício acadêmico, mas um vetor de modernização de serviços e impacto social.

Selecionamos o **Subtema 2 - Consumo Inteligente**, focando na inteligência social dos dados. Em um cenário onde a eficiência financeira é um direito a ser ampliado, nossa proposta buscou a modernização da gestão doméstica através de uma solução robusta e estrategicamente acessível.

## 2. Definição do Problema e Proposta de Valor

Identificamos um gargalo crítico na saúde financeira das famílias brasileiras: o dreno excessivo em alimentação, que frequentemente opera de forma invisível até comprometer a solvência do domicílio. O *SmartConsumer Insight Engine* foi projetado para expor essa ineficiência e oferecer uma rota de correção baseada em dados.

O quadro comparativo abaixo evidencia o abismo entre a realidade diagnosticada e os parâmetros de saúde financeira:

| Categoria | Cenário Identificado (Dreno) | Cenário Ideal (Regra 50-30-20) | Margem Crítica |
| :--- | :--- | :--- | :--- |
| Alimentação | 68% da renda líquida | 10% a 15% (Ideal) | Máximo de 30% (Alto Custo) |
| Impacto Relativo | ~7x o mínimo ideal | Referência de estabilidade | Limite de sustentabilidade |

Nossa proposta de valor reside na **acessibilidade estratégica**: transformar dados brutos em inteligência acionável, permitindo que o usuário identifique desequilíbrios antes que se tornem insolúveis, alinhando o consumo individual aos padrões de sustentabilidade econômica.

## 3. Arquitetura Técnica e Pipeline End-to-End (E2E)

Liderando Ciência de Dados, asseguramos que o Esquadrão 12 adotasse uma **arquitetura desacoplada**. A distinção clara entre a camada de armazenamento (SQLite) e a lógica de processamento (Python) não apenas cumpre os requisitos técnicos, mas garante a escalabilidade futura do ecossistema.

*** Ingestão e Estruturação (SQL):** Implementamos um pipeline robusto onde a proficiência em SQL foi demonstrada através de queries `SELECT` para consumo e manipulação da base de dados, garantindo integridade desde a origem.
*** Análise Exploratória (EDA) e Estatística:** A aplicação de estatística descritiva foi fundamental para o mapeamento de padrões e, crucialmente, para a identificação de outliers que distorceriam as predições financeiras.
*** Modelagem Preditiva (ML):** Optamos estrategicamente pela Regression (Regressão Linear). Embora modelos complexos tenham sido discutidos, priorizamos a **Explainability (XAI)**. Em produtos financeiros, a transparência do "porquê" de uma previsão é mais valiosa para o executivo e para o usuário do que a opacidade de uma rede neural profunda.
*** Interface e Visualização:** A escolha do **Streamlit** como camada de delivery transformou o pipeline E2E em uma ferramenta de suporte à decisão em tempo real.

## 4. Desenvolvimento do MVP e Interface no Streamlit

A maturidade técnica do Esquadrão 12 manifestou-se na transição estratégica da "Análise para o Produto". Seguindo os princípios da cultura de inovação — *começar pelo básico e sofisticar com base em feedback* — evoluímos um ambiente de experimentação estático (Jupyter Notebook) para uma aplicação dinâmica em produção.

Esta "Produtização" via Streamlit permitiu a implementação de **Simulações em Tempo Real**, onde o usuário interage com os dados e visualiza o impacto de suas decisões instantaneamente. Mantivemos a transparência metodológica em toda a interface, assegurando que o motor de insights não fosse uma "caixa-preta", mas um consultor financeiro digital auditável e confiável.

## 5. Estratégia de Storytelling e Apresentação Final

Nossa narrativa de 8 minutos foi construída sobre o pilar da **Inteligência Social**. Não apresentamos apenas métricas; contamos a jornada de superação de um dreno financeiro de 68% rumo à estabilidade. A Ética em IA foi um fio condutor, abordando a responsabilidade no tratamento de dados sensíveis e a proteção contra vieses algorítmicos.

A execução bem-sucedida foi fruto de uma estrutura organizacional clara:

*** Implementação:** Foco em código limpo e robustez do modelo de ML.
*** Documentação:** Garantia de rastreabilidade do pipeline.
*** Pitch e Business Case:** Tradução da complexidade técnica em valor de negócio, focando na celeridade da tomada de decisão.

## 6. Feedback da Banca e Reconhecimento

Nossa equipe consolidou sua posição entre os **10 melhores grupos** de um universo de 54 participantes. Esse resultado valida nossa visão de que a ciência de dados, quando orientada ao produto e ao impacto real, é um diferencial competitivo indiscutível.

O reconhecimento oficial da banca destacou:

"Transformaram análise em produto: aplicação em produção com experiência prática e transparência metodológica nos resultados."

Este feedback chancela nossa maturidade em equilibrar rigor técnico com entrega de valor executivo.

## 7. Conclusão e Próximos Passos

O *SmartConsumer Insight Engine* encerra este ciclo como um ativo de portfólio de alto nível, pronto para ser apresentado ao mercado e para gerar conexões estratégicas no LinkedIn. Adotamos a máxima de que "*o erro faz parte do aprendizado; errar rápido e corrigir rápido*" para atingir este nível de excelência em apenas quatro dias.

Acreditamos na **Inovação Aberta** como caminho para a evolução contínua. Este MVP é o primeiro passo para sistemas ainda mais sofisticados que visam a eficiência dos serviços e a ampliação do acesso a direitos financeiros básicos. A jornada do Grupo 12 prova que, com o pipeline correto e uma mentalidade de produto, dados transformam realidades.

[Voltar ao Repositório](../README.md)
