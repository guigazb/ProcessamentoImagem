from PIL import Image
import math
import cv2

def converter_cinza(imagem_pil):
    return imagem_pil.convert("L")

#Gradiente Magnitude Básica (Diferenças Finitas Simples)
def filtro_gradiente(imagem_pil):
    img = converter_cinza(imagem_pil)
    w, h = img.size
    pixels = img.load()
    nova_img = Image.new("L", (w, h))
    novos_pixels = nova_img.load()

    for x in range(w - 1):
        for y in range(h - 1):
            # Gradiente simples: pixel atual menos o próximo
            gx = pixels[x + 1, y] - pixels[x, y]
            gy = pixels[x, y + 1] - pixels[x, y]
            magnitude = int(math.sqrt(gx**2 + gy**2))
            novos_pixels[x, y] = min(255, max(0, magnitude))
    return nova_img

#Operador de Roberts (Máscaras 2x2 diagonais)
def filtro_roberts(imagem_pil):
    img = converter_cinza(imagem_pil)
    w, h = img.size
    pixels = img.load()
    nova_img = Image.new("L", (w, h))
    novos_pixels = nova_img.load()

    for x in range(w - 1):
        for y in range(h - 1):
            gx = pixels[x, y] - pixels[x + 1, y + 1]
            gy = pixels[x + 1, y] - pixels[x, y + 1]
            magnitude = int(math.sqrt(gx**2 + gy**2))
            novos_pixels[x, y] = min(255, max(0, magnitude))
    return nova_img

#Operador de Prewitt (Máscaras 3x3)
def filtro_prewitt(imagem_pil):
    img = converter_cinza(imagem_pil)
    w, h = img.size
    pixels = img.load()
    nova_img = Image.new("L", (w, h))
    novos_pixels = nova_img.load()

    for x in range(1, w - 1):
        for y in range(1, h - 1):
            gx = (pixels[x+1, y-1] + pixels[x+1, y] + pixels[x+1, y+1]) - \
                 (pixels[x-1, y-1] + pixels[x-1, y] + pixels[x-1, y+1])
            gy = (pixels[x-1, y+1] + pixels[x, y+1] + pixels[x+1, y+1]) - \
                 (pixels[x-1, y-1] + pixels[x, y-1] + pixels[x+1, y-1])
            magnitude = int(math.sqrt(gx**2 + gy**2))
            novos_pixels[x, y] = min(255, max(0, magnitude))
    return nova_img

#Operador de Sobel (Máscaras 3x3 com peso maior no centro)
def filtro_sobel(imagem_pil):
    img = converter_cinza(imagem_pil)
    w, h = img.size
    pixels = img.load()
    nova_img = Image.new("L", (w, h))
    novos_pixels = nova_img.load()

    for x in range(1, w - 1):
        for y in range(1, h - 1):
            gx = (pixels[x+1, y-1] + 2*pixels[x+1, y] + pixels[x+1, y+1]) - \
                 (pixels[x-1, y-1] + 2*pixels[x-1, y] + pixels[x-1, y+1])
            gy = (pixels[x-1, y+1] + 2*pixels[x, y+1] + pixels[x+1, y+1]) - \
                 (pixels[x-1, y-1] + 2*pixels[x, y-1] + pixels[x+1, y-1])
            magnitude = int(math.sqrt(gx**2 + gy**2))
            novos_pixels[x, y] = min(255, max(0, magnitude))
    return nova_img

#Laplaciano (Derivada de Segunda Ordem - Máscara padrão)
def filtro_laplaciano(imagem_pil):
    img = converter_cinza(imagem_pil)
    w, h = img.size
    pixels = img.load()
    nova_img = Image.new("L", (w, h))
    novos_pixels = nova_img.load()

    for x in range(1, w - 1):
        for y in range(1, h - 1):
            # Máscara: [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
            valor = (pixels[x, y-1] + pixels[x-1, y] + pixels[x+1, y] + pixels[x, y+1]) - (4 * pixels[x, y])
            # Como o Laplaciano pode dar negativo, uso o módulo
            novos_pixels[x, y] = min(255, max(0, abs(valor)))
    return nova_img

#Laplaciana da Gaussiana (LoG) + Cruzamento por Zero
#calcula o LoG e extrai as bordas verificando a mudança de sinal (Cruzamento por Zero)
def log_e_cruzamento_zero(imagem_pil, sigma=1.0):
    img = converter_cinza(imagem_pil)
    w, h = img.size
    pixels = img.load()
    
    tamanho = 5
    offset = tamanho // 2
    kernel = [[0.0] * tamanho for _ in range(tamanho)]
    
    for x in range(tamanho):
        for y in range(tamanho):
            dx = x - offset
            dy = y - offset

            normalizacao = -1 / (math.pi * sigma**4)
            expoente = -(dx**2 + dy**2) / (2 * sigma**2)
            kernel[x][y] = normalizacao * (1 - (dx**2 + dy**2) / (2 * sigma**2)) * math.exp(expoente)
            
    #mapa temporário de floats para armazenar os sinais (+ e -) do LoG
    mapa_log = [[0.0] * h for _ in range(w)]
    for x in range(offset, w - offset):
        for y in range(offset, h - offset):
            soma = 0.0
            for i in range(tamanho):
                for j in range(tamanho):
                    soma += pixels[x + i - offset, y + j - offset] * kernel[i][j]
            mapa_log[x][y] = soma

    #Cruzamento por Zero (Zero-Crossing)
    img_bordas = Image.new("L", (w, h))
    pixels_bordas = img_bordas.load()
    limiar = 1 # Evita detectar ruídos insignificantes
    
    for x in range(offset + 1, w - offset - 1):
        for y in range(offset + 1, h - offset - 1):
            val = mapa_log[x][y]
            # Vizinhos: Direita, Baixo, Diagonal
            vizinhos = [mapa_log[x+1][y], mapa_log[x][y+1], mapa_log[x+1][y+1]]
            
            for v in vizinhos:
                # Se houver mudança de sinal entre o pixel e o vizinho e a diferença for relevante
                if (val > 0 and v < 0) or (val < 0 and v > 0):
                    if abs(val - v) > limiar:
                        pixels_bordas[x, y] = 255
                        break
    return img_bordas

#Algoritmo de Canny
def filtro_canny(caminho_imagem):
    img = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None
    # Canny(imagem, limiar_inferior, limiar_superior)
    bordas = cv2.Canny(img, 100, 200)

    return Image.fromarray(bordas)

if __name__ == "__main__":
    caminho = "demolidor.jpeg"
    try:
        img_orig = Image.open(caminho)
        
        print("Processando Gradiente...")
        filtro_gradiente(img_orig).save("borda_gradiente.png")
        
        print("Processando Roberts...")
        filtro_roberts(img_orig).save("borda_roberts.png")
        
        print("Processando Prewitt...")
        filtro_prewitt(img_orig).save("borda_prewitt.png")
        
        print("Processando Sobel...")
        filtro_sobel(img_orig).save("borda_sobel.png")
        
        print("Processando Laplaciano...")
        filtro_laplaciano(img_orig).save("borda_laplaciano.png")
        
        print("Processando Laplaciana da Gaussiana + Cruzamento por Zero...")
        log_e_cruzamento_zero(img_orig).save("borda_log_cruzamento.png")
        
        print("Processando Canny (OpenCV)...")
        img_canny = filtro_canny(caminho)
        if img_canny:
            img_canny.save("borda_canny.png")
            
        print("Todos os filtros de borda foram aplicados e salvos!")
    except FileNotFoundError:
        print(f"Erro: Crie ou insira uma imagem válida chamada '{caminho}' no diretório.")