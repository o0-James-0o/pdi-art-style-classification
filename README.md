# 🖼️ Classificação de Estilos Artísticos em Pinturas Reais com Pipeline Clássico de PDI

<p align="center">
  <img src="assets/project_overview.png" alt="Visão geral do projeto" width="100%">
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-0B1F5B?style=for-the-badge&logo=python&logoColor=white">
  <img alt="PDI" src="https://img.shields.io/badge/PDI-Pipeline%20Cl%C3%A1ssico-0B1F5B?style=for-the-badge">
  <img alt="Dataset" src="https://img.shields.io/badge/Dataset-WikiArt-0B1F5B?style=for-the-badge">
  <img alt="Implementação" src="https://img.shields.io/badge/Implementa%C3%A7%C3%A3o-Manual-0B1F5B?style=for-the-badge">
  <img alt="Modelo" src="https://img.shields.io/badge/Modelo-KNN%20%2B%20Regress%C3%A3o%20Log%C3%ADstica-0B1F5B?style=for-the-badge">
</p>

> Projeto aplicado de **Processamento Digital de Imagens** voltado à análise e classificação de **estilos artísticos em pinturas reais**, usando descritores clássicos implementados manualmente e modelos simples de aprendizado de máquina.

---

## 📌 Descrição do projeto

Este repositório apresenta um pipeline clássico de **Processamento Digital de Imagens (PDI)** aplicado à classificação de pinturas reais do **WikiArt** em quatro estilos artísticos: **Baroque**, **Cubism**, **Impressionism** e **Realism**.

A proposta prioriza o entendimento dos algoritmos clássicos: as principais etapas foram implementadas manualmente, sem uso de funções prontas para convolução, Sobel, Otsu, morfologia, DCT, quantização, entropia e extração de características.

O classificador recebe um vetor com **97 descritores numéricos** extraídos de cada imagem e realiza a predição do estilo artístico com modelos como **KNN** e **Regressão Logística**.

---

## 🎯 Objetivo

Desenvolver e avaliar um sistema capaz de **extrair características visuais clássicas de pinturas reais** e utilizá-las em modelos simples de aprendizado de máquina para classificar estilos artísticos.

<table width="100%">
  <tr>
    <th width="28%" align="center">Aspecto analisado</th>
    <th width="72%" align="center">Relevância no projeto</th>
  </tr>
  <tr>
    <td><strong>Cor</strong></td>
    <td>Representa padrões cromáticos presentes nos diferentes estilos artísticos.</td>
  </tr>
  <tr>
    <td><strong>Bordas</strong></td>
    <td>Captura contornos, fragmentações e estruturas visuais por meio do operador de Sobel.</td>
  </tr>
  <tr>
    <td><strong>Regiões segmentadas</strong></td>
    <td>Permite descrever áreas claras, escuras e componentes conectados após Otsu e morfologia.</td>
  </tr>
  <tr>
    <td><strong>Frequência</strong></td>
    <td>Analisa energia em baixa, média e alta frequência com DCT em blocos 8x8.</td>
  </tr>
</table>

---

## ✅ Requisitos do projeto atendidos

<table width="100%">
  <tr>
    <th width="10%" align="center">Item</th>
    <th width="32%" align="center">Requisito solicitado</th>
    <th width="58%" align="center">Como foi atendido</th>
  </tr>
  <tr>
    <td align="center">🗂️</td>
    <td><strong>Dataset relacionado ao tema</strong></td>
    <td>Recorte real do WikiArt com 200 pinturas balanceadas entre quatro estilos.</td>
  </tr>
  <tr>
    <td align="center">🛠️</td>
    <td><strong>Transformação de imagem</strong></td>
    <td>Conversão RGB → cinza, filtragem espacial e detecção de bordas por Sobel.</td>
  </tr>
  <tr>
    <td align="center">📦</td>
    <td><strong>Compressão / informação</strong></td>
    <td>DCT 8x8, quantização, entropia, MSE, PSNR e percentual de coeficientes zerados.</td>
  </tr>
  <tr>
    <td align="center">🎚️</td>
    <td><strong>Segmentação</strong></td>
    <td>Limiarização automática de Otsu implementada manualmente.</td>
  </tr>
  <tr>
    <td align="center">⬛</td>
    <td><strong>Morfologia</strong></td>
    <td>Dilatação, erosão, abertura e fechamento com elemento estruturante 3x3.</td>
  </tr>
  <tr>
    <td align="center">🤖</td>
    <td><strong>Aprendizado de máquina</strong></td>
    <td>Classificação com KNN e Regressão Logística usando descritores extraídos.</td>
  </tr>
</table>

---

## 🧰 Recursos técnicos utilizados

A tabela abaixo resume os principais recursos técnicos do projeto. As bibliotecas de imagem foram usadas de forma restrita, preservando a implementação manual das etapas centrais de PDI.

---

<table width="100%">
  <tr>
    <th width="24%" align="center">Recurso</th>
    <th width="34%" align="center">Uso no projeto</th>
    <th width="42%" align="center">Observação técnica</th>
  </tr>
  <tr>
    <td><strong>Python</strong></td>
    <td>Linguagem principal do projeto.</td>
    <td>Usada para implementar o pipeline, extrair características e treinar modelos.</td>
  </tr>
  <tr>
    <td><strong>OpenCV</strong></td>
    <td>Leitura e escrita de imagens.</td>
    <td>Não foi usado para resolver as etapas principais, como Sobel, Otsu, morfologia ou DCT.</td>
  </tr>
  <tr>
    <td><strong>NumPy</strong></td>
    <td>Manipulação matricial.</td>
    <td>Base para cálculos numéricos, percursos em matriz e vetores de características.</td>
  </tr>
  <tr>
    <td><strong>Pandas</strong></td>
    <td>Organização de resultados.</td>
    <td>Usado para salvar e ler tabelas de características, métricas e comparação de modelos.</td>
  </tr>
  <tr>
    <td><strong>scikit-learn</strong></td>
    <td>Aprendizado de máquina.</td>
    <td>Usado apenas na etapa permitida de treino e avaliação dos modelos.</td>
  </tr>
  <tr>
    <td><strong>Matplotlib</strong></td>
    <td>Visualização de resultados.</td>
    <td>Gera gráficos, matriz de confusão e imagens de apoio para análise.</td>
  </tr>
</table>

---

## 🗂️ Dataset e recorte experimental

O projeto utiliza um recorte enxuto de **200 pinturas reais** do WikiArt. O conjunto foi mantido balanceado para reduzir o custo computacional e preservar a comparação entre classes.

<table width="100%">
  <tr>
    <th width="32%" align="center">Classe</th>
    <th width="20%" align="center">Quantidade</th>
    <th width="24%" align="center">Treino</th>
    <th width="24%" align="center">Teste</th>
  </tr>
  <tr>
    <td><strong>Baroque</strong></td>
    <td align="center">50</td>
    <td align="center">35</td>
    <td align="center">15</td>
  </tr>
  <tr>
    <td><strong>Cubism</strong></td>
    <td align="center">50</td>
    <td align="center">35</td>
    <td align="center">15</td>
  </tr>
  <tr>
    <td><strong>Impressionism</strong></td>
    <td align="center">50</td>
    <td align="center">35</td>
    <td align="center">15</td>
  </tr>
  <tr>
    <td><strong>Realism</strong></td>
    <td align="center">50</td>
    <td align="center">35</td>
    <td align="center">15</td>
  </tr>
  <tr>
    <td><strong>Total</strong></td>
    <td align="center"><strong>200</strong></td>
    <td align="center"><strong>140</strong></td>
    <td align="center"><strong>60</strong></td>
  </tr>
</table>

### Estrutura local esperada do dataset

```text
pdi-art-style-classification/
└── data/
    └── raw/
        ├── Baroque/
        ├── Cubism/
        ├── Impressionism/
        └── Realism/
```

> As imagens reais do WikiArt não são versionadas no repositório. Use `baixar_recorte_wikiart.py` para reproduzir o recorte localmente.

---

## 🧠 Metodologia

A metodologia adotada é **aplicada, experimental e quantitativa**. O fluxo segue a lógica de reconhecimento estatístico de padrões: definir o problema, selecionar dados, pré-processar imagens, extrair descritores, treinar modelos e interpretar resultados.

<p align="center">
  <img src="assets/metodologia_readme.png" alt="Metodologia do projeto" width="100%">
</p>

---

## 🔁 Pipeline clássico proposto

Todas as imagens seguem a mesma sequência de processamento. O modelo não recebe pixels brutos: ele recebe **descritores extraídos manualmente** a partir das etapas clássicas de PDI.

<p align="center">
  <img src="assets/pipeline_classico_readme.png" alt="Pipeline clássico de PDI" width="100%">
</p>

<table width="100%">
  <tr>
    <th width="25%" align="center">Etapa</th>
    <th width="75%" align="center">Função no pipeline</th>
  </tr>
  <tr>
    <td><strong>Imagem original</strong></td>
    <td>Entrada colorida do dataset WikiArt.</td>
  </tr>
  <tr>
    <td><strong>Escala de cinza</strong></td>
    <td>Simplifica a análise estrutural e tonal da pintura.</td>
  </tr>
  <tr>
    <td><strong>Filtro espacial</strong></td>
    <td>Suaviza pequenas variações locais antes da extração de bordas.</td>
  </tr>
  <tr>
    <td><strong>Sobel</strong></td>
    <td>Detecta bordas por gradientes horizontal e vertical.</td>
  </tr>
  <tr>
    <td><strong>Otsu</strong></td>
    <td>Segmenta automaticamente regiões claras e escuras.</td>
  </tr>
  <tr>
    <td><strong>Morfologia</strong></td>
    <td>Refina a máscara binária por dilatação, erosão, abertura e fechamento.</td>
  </tr>
  <tr>
    <td><strong>DCT / Quantização</strong></td>
    <td>Analisa frequência, compressibilidade e perda de informação.</td>
  </tr>
  <tr>
    <td><strong>Features</strong></td>
    <td>Concatena estatísticas, histogramas, bordas, segmentação e frequência.</td>
  </tr>
  <tr>
    <td><strong>KNN</strong></td>
    <td>Classifica a pintura de acordo com o vetor de características.</td>
  </tr>
</table>

---

## 🛠️ Implementações manuais de PDI

As principais técnicas de PDI foram implementadas manualmente com laços, operações matriciais e fórmulas clássicas. O OpenCV foi usado somente para leitura e escrita de imagens.

<table width="100%">
  <tr>
    <th width="30%" align="center">Técnica</th>
    <th width="70%" align="center">Implementação realizada</th>
  </tr>
  <tr>
    <td><strong>RGB → cinza</strong></td>
    <td>Combinação ponderada dos canais RGB.</td>
  </tr>
  <tr>
    <td><strong>Redimensionamento</strong></td>
    <td>Interpolação bilinear manual.</td>
  </tr>
  <tr>
    <td><strong>Convolução 2D</strong></td>
    <td>Aplicação manual de kernels sobre a vizinhança da imagem.</td>
  </tr>
  <tr>
    <td><strong>Filtro espacial</strong></td>
    <td>Máscara média ou gaussiana 3x3 implementada por convolução.</td>
  </tr>
  <tr>
    <td><strong>Sobel</strong></td>
    <td>Máscaras `Gx` e `Gy`, seguidas da magnitude do gradiente.</td>
  </tr>
  <tr>
    <td><strong>Histograma e entropia</strong></td>
    <td>Contagem de intensidades e cálculo por distribuição de probabilidades.</td>
  </tr>
  <tr>
    <td><strong>Otsu</strong></td>
    <td>Teste de limiares e maximização da variância entre classes.</td>
  </tr>
  <tr>
    <td><strong>Morfologia</strong></td>
    <td>Erosão, dilatação, abertura e fechamento com elemento estruturante 3x3.</td>
  </tr>
  <tr>
    <td><strong>DCT 8x8 e IDCT</strong></td>
    <td>Transformada em blocos, quantização e reconstrução.</td>
  </tr>
</table>

---

## 🧩 Técnicas em destaque

### 1. Transformação espacial e bordas por Sobel

<p align="center">
  <img src="assets/tecnica_transformacao_readme.png" alt="Técnica de transformação de imagem" width="100%">
</p>

A transformação espacial converte a imagem para cinza, aplica suavização e calcula bordas. Esses resultados alimentam descritores como densidade de bordas, média do gradiente e variação estrutural da pintura.

### 2. Segmentação por Otsu

<p align="center">
  <img src="assets/tecnica_segmentacao_readme.png" alt="Técnica de segmentação" width="100%">
</p>

A segmentação por Otsu calcula o histograma e escolhe o limiar que melhor separa regiões claras e escuras. A máscara binária gerada é usada na morfologia e na extração de descritores estruturais.

### 3. Morfologia binária

<p align="center">
  <img src="assets/tecnica_morfologia_readme.png" alt="Técnica de morfologia" width="100%">
</p>

A morfologia atua sobre a máscara binária. O fechamento, formado por dilatação seguida de erosão, preenche pequenas falhas e melhora a continuidade das regiões segmentadas.

### 4. Compressão com DCT e quantização

<p align="center">
  <img src="assets/tecnica_compressao_readme.png" alt="Técnica de compressão" width="100%">
</p>

A DCT em blocos 8x8 foi usada para analisar a energia no domínio da frequência. A quantização reduz a precisão dos coeficientes e permite medir MSE, PSNR, entropia e coeficientes zerados.

---

## 📊 Características extraídas

Cada imagem foi representada por um vetor de **97 características numéricas**.

<table width="100%">
  <tr>
    <th width="26%" align="center">Grupo</th>
    <th width="74%" align="center">Exemplos de características</th>
  </tr>
  <tr>
    <td><strong>Cor</strong></td>
    <td>Média, desvio, assimetria e curtose nos canais RGB.</td>
  </tr>
  <tr>
    <td><strong>Histogramas</strong></td>
    <td>Histogramas normalizados RGB e escala de cinza.</td>
  </tr>
  <tr>
    <td><strong>Intensidade</strong></td>
    <td>Média, desvio, entropia e estatísticas da imagem em cinza.</td>
  </tr>
  <tr>
    <td><strong>Bordas</strong></td>
    <td>Densidade de bordas, média e desvio do gradiente.</td>
  </tr>
  <tr>
    <td><strong>Segmentação</strong></td>
    <td>Limiar de Otsu, proporção de foreground/background e regiões segmentadas.</td>
  </tr>
  <tr>
    <td><strong>Morfologia</strong></td>
    <td>Componentes conectados e maior região segmentada.</td>
  </tr>
  <tr>
    <td><strong>Frequência / compressão</strong></td>
    <td>Energia DCT, entropia quantizada, MSE, PSNR e coeficientes zerados.</td>
  </tr>
</table>

---

## 🤖 Modelos de aprendizado de máquina

Foram avaliados modelos simples e interpretáveis, mantendo o foco principal no pipeline clássico de PDI.

<table width="100%">
  <tr>
    <th width="28%" align="center">Modelo</th>
    <th width="72%" align="center">Justificativa</th>
  </tr>
  <tr>
    <td><strong>KNN</strong></td>
    <td>Classificador simples baseado em distância entre vetores de características.</td>
  </tr>
  <tr>
    <td><strong>Regressão Logística</strong></td>
    <td>Modelo linear usado como comparação quantitativa.</td>
  </tr>
</table>

Valores de `k` avaliados no KNN:

```text
k = 1, 3, 5, 7, 9, 11
```

---

## 📈 Resultados quantitativos

O melhor desempenho foi obtido com o modelo **KNN_k=9**.

<p align="center">
  <img src="assets/knn_k_variation.png" alt="Variação do K no KNN" width="85%">
</p>

### Comparação entre modelos

<table width="100%">
  <tr>
    <th width="22%" align="center">Modelo</th>
    <th width="18%" align="center">Acurácia</th>
    <th width="20%" align="center">Precisão macro</th>
    <th width="20%" align="center">Revocação macro</th>
    <th width="20%" align="center">F1 macro</th>
  </tr>
  <tr>
    <td><strong>KNN_k=9</strong></td>
    <td align="center"><strong>58.33%</strong></td>
    <td align="center"><strong>59.64%</strong></td>
    <td align="center"><strong>58.33%</strong></td>
    <td align="center"><strong>56.12%</strong></td>
  </tr>
  <tr>
    <td>KNN_k=5</td>
    <td align="center">53.33%</td>
    <td align="center">54.32%</td>
    <td align="center">53.33%</td>
    <td align="center">50.35%</td>
  </tr>
  <tr>
    <td>KNN_k=11</td>
    <td align="center">53.33%</td>
    <td align="center">53.46%</td>
    <td align="center">53.33%</td>
    <td align="center">49.98%</td>
  </tr>
  <tr>
    <td>Regressão Logística</td>
    <td align="center">50.00%</td>
    <td align="center">49.26%</td>
    <td align="center">50.00%</td>
    <td align="center">48.59%</td>
  </tr>
</table>

### Métricas por classe — melhor modelo

<table width="100%">
  <tr>
    <th width="28%" align="center">Classe</th>
    <th width="18%" align="center">Precisão</th>
    <th width="18%" align="center">Revocação</th>
    <th width="18%" align="center">F1-score</th>
    <th width="18%" align="center">Suporte</th>
  </tr>
  <tr>
    <td><strong>Baroque</strong></td>
    <td align="center">62.50%</td>
    <td align="center">66.67%</td>
    <td align="center">64.52%</td>
    <td align="center">15</td>
  </tr>
  <tr>
    <td><strong>Cubism</strong></td>
    <td align="center">77.78%</td>
    <td align="center">46.67%</td>
    <td align="center">58.33%</td>
    <td align="center">15</td>
  </tr>
  <tr>
    <td><strong>Impressionism</strong></td>
    <td align="center">53.85%</td>
    <td align="center">93.33%</td>
    <td align="center">68.29%</td>
    <td align="center">15</td>
  </tr>
  <tr>
    <td><strong>Realism</strong></td>
    <td align="center">44.44%</td>
    <td align="center">26.67%</td>
    <td align="center">33.33%</td>
    <td align="center">15</td>
  </tr>
</table>

---

## 🧪 Resultados de DCT, compressão e entropia

<table width="100%">
  <tr>
    <th width="16%" align="center">Classe</th>
    <th width="14%" align="center">Entropia</th>
    <th width="14%" align="center">Coef. zerados</th>
    <th width="14%" align="center">MSE</th>
    <th width="14%" align="center">PSNR</th>
    <th width="14%" align="center">Energia baixa</th>
    <th width="14%" align="center">Energia média</th>
  </tr>
  <tr>
    <td><strong>Baroque</strong></td>
    <td align="center">6.42</td>
    <td align="center">85.14%</td>
    <td align="center">11.64</td>
    <td align="center">37.80</td>
    <td align="center">0.9752</td>
    <td align="center">0.0241</td>
  </tr>
  <tr>
    <td><strong>Cubism</strong></td>
    <td align="center">7.22</td>
    <td align="center">79.03%</td>
    <td align="center">20.89</td>
    <td align="center">35.11</td>
    <td align="center">0.9261</td>
    <td align="center">0.0712</td>
  </tr>
  <tr>
    <td><strong>Impressionism</strong></td>
    <td align="center">7.16</td>
    <td align="center">81.97%</td>
    <td align="center">15.32</td>
    <td align="center">36.52</td>
    <td align="center">0.9511</td>
    <td align="center">0.0471</td>
  </tr>
  <tr>
    <td><strong>Realism</strong></td>
    <td align="center">7.12</td>
    <td align="center">82.11%</td>
    <td align="center">15.58</td>
    <td align="center">36.39</td>
    <td align="center">0.9617</td>
    <td align="center">0.0370</td>
  </tr>
</table>

**Interpretação:** Cubism apresentou maior entropia e maior energia média, indicando maior variação visual e fragmentação estrutural. Baroque concentrou mais energia em baixa frequência e teve maior taxa de coeficientes zerados.

---

## 🧾 Matriz de confusão

<p align="center">
  <img src="assets/confusion_matrix_best.png" alt="Matriz de confusão" width="75%">
</p>

<table width="100%">
  <tr>
    <th width="30%" align="center">Observação</th>
    <th width="70%" align="center">Interpretação</th>
  </tr>
  <tr>
    <td><strong>Impressionism</strong></td>
    <td>Foi a classe mais reconhecida, com 14 acertos em 15 imagens.</td>
  </tr>
  <tr>
    <td><strong>Baroque</strong></td>
    <td>Apresentou bom desempenho, com 10 acertos em 15 imagens.</td>
  </tr>
  <tr>
    <td><strong>Realism</strong></td>
    <td>Teve maior confusão, principalmente com Baroque e Impressionism.</td>
  </tr>
  <tr>
    <td><strong>Leitura geral</strong></td>
    <td>Os descritores clássicos capturam padrões úteis, mas estilos artísticos podem compartilhar características visuais semelhantes.</td>
  </tr>
</table>

---

## 🖼️ Resultados visuais do pipeline

As imagens abaixo mostram exemplos reais processados pelo pipeline. Cada figura apresenta etapas como imagem original, escala de cinza, filtro espacial, Sobel, Otsu, morfologia, DCT e reconstrução.

<table width="100%">
  <tr>
    <th width="50%" align="center">Baroque</th>
    <th width="50%" align="center">Cubism</th>
  </tr>
  <tr>
    <td align="center"><img src="assets/pipeline_baroque.png" width="100%"></td>
    <td align="center"><img src="assets/pipeline_cubism.png" width="100%"></td>
  </tr>
</table>

<table width="100%">
  <tr>
    <th width="50%" align="center">Impressionism</th>
    <th width="50%" align="center">Realism</th>
  </tr>
  <tr>
    <td align="center"><img src="assets/pipeline_impressionism.png" width="100%"></td>
    <td align="center"><img src="assets/pipeline_realism.png" width="100%"></td>
  </tr>
</table>

---

## 📁 Estrutura do repositório

Estrutura atual versionada no GitHub:

```text
pdi-art-style-classification/
│
├── assets/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── features.py
│   ├── io_utils.py
│   ├── pdi_manual.py
│   └── visualize.py
│
├── .gitignore
├── README.md
├── baixar_recorte_wikiart.py
├── download_wikiart_huggingface.py
├── requirements.txt
├── requirements_optional.txt
├── run_all.py
├── run_extract_features.py
└── run_train_models.py
```

Pastas geradas localmente durante a execução:

```text
data/raw/      # pinturas reais baixadas do WikiArt
results/       # métricas, tabelas, imagens e CSVs gerados pelo pipeline
```

---

## ▶️ Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/o0-James-0o/pdi-art-style-classification.git
cd pdi-art-style-classification
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Baixar o recorte do WikiArt

```bash
python baixar_recorte_wikiart.py
```

Estrutura esperada após o download:

```text
data/raw/Baroque/
data/raw/Cubism/
data/raw/Impressionism/
data/raw/Realism/
```

### 4. Rodar o pipeline completo

```bash
python run_all.py
```

### 5. Rodar por etapas

```bash
python run_extract_features.py
python run_train_models.py
```

---

## 📦 Saídas geradas

<table width="100%">
  <tr>
    <th width="34%" align="center">Arquivo</th>
    <th width="66%" align="center">Conteúdo</th>
  </tr>
  <tr>
    <td><code>features.csv</code></td>
    <td>Vetores de características extraídos de cada imagem.</td>
  </tr>
  <tr>
    <td><code>compression_metrics.csv</code></td>
    <td>Métricas de DCT, quantização, entropia, MSE e PSNR.</td>
  </tr>
  <tr>
    <td><code>model_comparison.csv</code></td>
    <td>Comparação entre KNN e Regressão Logística.</td>
  </tr>
  <tr>
    <td><code>classification_report_best.csv</code></td>
    <td>Métricas por classe do melhor modelo.</td>
  </tr>
  <tr>
    <td><code>confusion_matrix_best.png</code></td>
    <td>Matriz de confusão do melhor modelo.</td>
  </tr>
  <tr>
    <td><code>knn_k_variation.png</code></td>
    <td>Gráfico de variação do valor de k no KNN.</td>
  </tr>
  <tr>
    <td><code>visual_pipeline/</code></td>
    <td>Figuras visuais das etapas do pipeline por classe.</td>
  </tr>
</table>

---

## ✅ Conclusão

O projeto demonstrou que técnicas clássicas de Processamento Digital de Imagens podem ser integradas em um fluxo único, interpretável e aplicado a pinturas reais. Mesmo com desempenho moderado, o melhor modelo (**KNN_k=9**) superou o acaso esperado para quatro classes balanceadas e evidenciou que descritores manuais carregam informação discriminativa sobre estilos artísticos.

<table width="100%">
  <tr>
    <th width="28%" align="center">Resultado</th>
    <th width="72%" align="center">Interpretação</th>
  </tr>
  <tr>
    <td><strong>Melhor modelo</strong></td>
    <td>KNN_k=9 obteve o melhor desempenho geral entre as configurações avaliadas.</td>
  </tr>
  <tr>
    <td><strong>Acurácia</strong></td>
    <td>58.33%, acima do acaso esperado de 25% para quatro classes balanceadas.</td>
  </tr>
  <tr>
    <td><strong>Interpretação</strong></td>
    <td>Características de borda, textura, segmentação e frequência contribuíram para separar estilos artísticos.</td>
  </tr>
  <tr>
    <td><strong>Classes</strong></td>
    <td>Impressionism e Baroque foram mais reconhecidas; Realism apresentou maior confusão.</td>
  </tr>
</table>

---

## 👨‍💻 Autoria

<div align="left">
  <img src="https://github.com/o0-James-0o.png" alt="Avatar James Taylor" width="72" height="72" align="middle">
  &nbsp;&nbsp;
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=18&pause=1000&color=A78BFA&vCenter=true&multiline=false&width=760&height=72&lines=James+Taylor+%7C+Estudante+de+Ci%C3%AAncia+da+Computa%C3%A7%C3%A3o+%7C+PDI+e+Ciberseguran%C3%A7a." alt="James Taylor | Estudante de Ciência da Computação | PDI e Cibersegurança" align="middle">
</div>

---
