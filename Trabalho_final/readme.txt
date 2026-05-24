Autor: Guilherme Barrio Nascimento
Disciplina: Processamento de Imagens
Professor: Aristofanes Correa Silva

Trabalho final da Disciplina

Classificação de imagens de galáxias, usando CNNs e transfer learning

Requisitos: 
    - Python Instalado e configurado

Para executar o código: Python Main.py

usando dataset galaxyzoo 2 (https://www.kaggle.com/datasets/jaimetrickz/galaxy-zoo-2-images)

Método proposto:
1 . Segmentação e máscaras: thresholding adaptativo para isolar galáxia do fundo
Limiarização de Otsu (Otsu's Thresholding): Este algoritmo calcula automaticamente o limiar ideal para separar o objeto (galáxia) 
do fundo, minimizando a variância dentro das classes.

Operações Morfológicas: Após binarizar, uso Abertura (Erosão seguida de Dilatação) para eliminar pequenos pontos de luz 
(estrelas de fundo) e Fechamento para tapar "buracos" dentro da própria galáxia.

2. Redução de ruído: filtro da mediana, estimativa de fundo e CLAHE
Filtro Mediana: a mediana é excelente para remover "sal e pimenta" (pontos brancos isolados) preservando a estrutura dos braços 
espirais da galáxia.

Filtro de Estimativa de Fundo: estimar o brilho do céu e subtraí-lo para que o fundo fique o mais próximo possível do zero 
absoluto (preto puro).

CLAHE (Contrast Limited Adaptive Histogram Equalization): Ao contrário da equalização global, o CLAHE divide a imagem em pequenos 
blocos e equaliza cada um. Isso revela as texturas dos braços espirais e das faixas de poeira sem saturar o núcleo.

3. Extrair atributos morfológicos: concentração, assimetria e suavidade (CAS), usando GLCM (captura textura) e momentos de HU 
(identifica galáxia independente da rotação ou escala)

4. Treinamento com Rede CNN: fusão de dados ( imagem original em um ramo, atributos classicos em outro), treinar com galaxyzoo 2 
e teste com imagens de datasets dos telescópios james webb, hubb, etc, para testar a capacidade do modelo de generalização

