import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

def ler_pgm_ascii(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        print(f"Aviso: Arquivo '{caminho_arquivo}' não encontrado.")
        return None

    with open(caminho_arquivo, 'r') as f:
        linhas = f.readlines()

    # Remove comentários (linhas que começam com #) e junta todos os valores
    valores = []
    for linha in linhas:
        linha = linha.strip()
        if linha and not linha.startswith('#'):
            valores.extend(linha.split())

    # O cabeçalho PGM P2 tem: "P2", largura, altura, valor_maximo
    if valores[0] != 'P2':
        raise ValueError("O formato não é PGM ASCII (P2).")

    largura = int(valores[1])
    altura = int(valores[2])
    # valores[3] é o valor máximo (geralmente 255), os pixels começam no índice 4
    
    pixels = np.array([int(v) for v in valores[4:]], dtype=np.uint8)
    imagem_matriz = pixels.reshape((altura, largura))
    
    return imagem_matriz

def salvar_como_jpeg(matriz_imagem, nome_saida):
    if matriz_imagem is None:
        return
    
    imagem_pil = Image.fromarray(matriz_imagem)
    imagem_pil.save(nome_saida)
    print(f"Imagem salva como: {nome_saida}")

def principal():
    print("Iniciando conversão e visualização...")

    img_original = ler_pgm_ascii('Quantizacao\entrada2.pgm')
    img_uniforme = ler_pgm_ascii('Quantizacao\saida_uniforme.pgm')
    img_linear = ler_pgm_ascii('Quantizacao\saida_linear.pgm')

    if img_original is None:
        print("Erro: A imagem original não foi encontrada. Rode o algoritmo primeiro!")
        return

    salvar_como_jpeg(img_original, 'resultado_original.jpg')
    if img_uniforme is not None: salvar_como_jpeg(img_uniforme, 'resultado_uniforme.jpg')
    if img_linear is not None: salvar_como_jpeg(img_linear, 'resultado_linear.jpg')

    # Montar o Mosaico de Comparação (Matplotlib)
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    
    # Configurações do plot original
    ax[0].imshow(img_original, cmap='gray', vmin=0, vmax=255)
    ax[0].set_title('1. Imagem Original')
    ax[0].axis('off')

    # Configurações do plot Uniforme
    if img_uniforme is not None:
        ax[1].imshow(img_uniforme, cmap='gray', vmin=0, vmax=255)
        ax[1].set_title('2. Quantização Uniforme\n(Corte cego)')
        ax[1].axis('off')

    # Configurações do plot Linear
    if img_linear is not None:
        ax[2].imshow(img_linear, cmap='gray', vmin=0, vmax=255)
        ax[2].set_title('3. Quantização Linear\n(Adaptada ao Min/Max)')
        ax[2].axis('off')

    plt.tight_layout()
    print("Abrindo janela de visualização. Feche a janela para encerrar o script.")
    plt.show()

if __name__ == "__main__":
    principal()