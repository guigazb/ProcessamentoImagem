from PIL import Image
import random

def converter_cinza(imagem_pil):
    return imagem_pil.convert("L")

def dithering_aleatorio(imagem_pil):
    img = converter_cinza(imagem_pil)
    largura, altura = img.size
    pixels = img.load()
    
    nova_img = Image.new("1", (largura, altura)) # "1" para Pixel Binário (P&B)
    novos_pixels = nova_img.load()
    
    # Cada pixel é comparado com um valor aleatório entre 0 e 255
    for x in range(largura):
        for y in range(altura):
            limiar = random.randint(0, 255)
            novos_pixels[x, y] = 255 if pixels[x, y] > limiar else 0
            
    return nova_img

def dithering_mediano(imagem_pil):
    img = converter_cinza(imagem_pil)
    largura, altura = img.size
    pixels = img.load()
    
    nova_img = Image.new("1", (largura, altura))
    novos_pixels = nova_img.load()

    # Usa o valor 128 (média do range) como limiar fixo
    for x in range(largura):
        for y in range(altura):
            # Se for maior que o meio do caminho (128), fica branco
            novos_pixels[x, y] = 255 if pixels[x, y] > 128 else 0
            
    return nova_img

def dithering_ordenado(imagem_pil):
    img = converter_cinza(imagem_pil)
    largura, altura = img.size
    pixels = img.load()
    # Usa uma matriz de padrões fixos para decidir o limiar
    # Matriz de Bayer 2x2 normalizada para o range 0-255
    # Matriz original: [[0, 2], [3, 1]] -> (valor / 4) * 255
    bayer = [
        [0, 128],
        [192, 64]
    ]
    
    nova_img = Image.new("1", (largura, altura))
    novos_pixels = nova_img.load()
    
    for x in range(largura):
        for y in range(altura):
            limiar = bayer[x % 2][y % 2]
            novos_pixels[x, y] = 255 if pixels[x, y] > limiar else 0
            
    return nova_img

def dithering_floyd_steinberg(imagem_pil):
    img = imagem_pil.convert("L")
    largura, altura = img.size
    
    #lista plana de pixels, converte para float para os cálculos de erro não estourarem 0-255
    pixels = list(img.getdata())
    
    for y in range(altura):
        for x in range(largura):
            idx = y * largura + x
            
            velho_pixel = pixels[idx]
            novo_pixel = 255 if velho_pixel > 128 else 0
            pixels[idx] = novo_pixel
            
            erro = velho_pixel - novo_pixel
            
            # Difusão do erro para os vizinhos
            # Pixel à direita [x + 1, y]
            if x + 1 < largura:
                pixels[idx + 1] += erro * 7 / 16
            
            # Pixel abaixo à esquerda [x - 1, y + 1]
            if x - 1 >= 0 and y + 1 < altura:
                pixels[idx + largura - 1] += erro * 3 / 16
            
            # Pixel abaixo [x, y + 1]
            if y + 1 < altura:
                pixels[idx + largura] += erro * 5 / 16
            
            # Pixel abaixo à direita [x + 1, y + 1]
            if x + 1 < largura and y + 1 < altura:
                pixels[idx + largura + 1] += erro * 1 / 16
                
    nova_img = Image.new("1", (largura, altura))
    pixels_finais = [int(p) for p in pixels]
    nova_img.putdata(pixels_finais)
    
    return nova_img

if __name__ == "__main__":
    try:
        img_input = Image.open("demolidor.jpeg")
        
        dithering_aleatorio(img_input).save("d_aleatorio.png")
        dithering_mediano(img_input).save("d_mediano.png")
        dithering_ordenado(img_input).save("d_ordenado.png")
        dithering_floyd_steinberg(img_input).save("d_floyd.png")
        
        print("Algoritmos de Dithering aplicados com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")