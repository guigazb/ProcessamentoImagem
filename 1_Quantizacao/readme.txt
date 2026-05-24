Autor: Guilherme Barrio Nascimento
Disciplina: Processamento de Imagens
Professor: Ari

Atividade: Implementação de dois algoritmos de quantização de imagem

Foram implementados os algoritmos de quantização linear e uniforme, com duas entradas de exemplo
as imagens foram convertidas do formato jpeg para pgm ascii P2, para facilitar a Implementação

Requisitos: 
    - Python instalado
    - C++ instalado e configurado (caso não tenha, o executável contido no diretório já cria os arquivos de saída esperado)

para compilar: g++ -o meu_quantizador main.cpp LinearQuantization.cpp UniformQuantization.cpp
para executar o código: ./quantizador.exe

para visualizar o resultado: python visualizador.py