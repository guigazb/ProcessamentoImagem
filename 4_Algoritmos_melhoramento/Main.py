from PIL import Image
import math

def filtro_media(imagem_pil, tamanho_janela=3):
    largura, altura = imagem_pil.size
    pixels = imagem_pil.load()
    nova_imagem = Image.new("RGB", (largura, altura))
    novos_pixels = nova_imagem.load()
    
    offset = tamanho_janela // 2

    for x in range(offset, largura - offset):
        for y in range(offset, altura - offset):
            soma_r, soma_g, soma_b = 0, 0, 0
            
            for i in range(-offset, offset + 1):
                for j in range(-offset, offset + 1):
                    r, g, b = pixels[x + i, y + j]
                    soma_r += r
                    soma_g += g
                    soma_b += b
            
            num_pixels = tamanho_janela ** 2
            novos_pixels[x, y] = (
                soma_r // num_pixels,
                soma_g // num_pixels,
                soma_b // num_pixels
            )
            
    return nova_imagem

def filtro_mediana(imagem_pil, tamanho_janela=3):
    largura, altura = imagem_pil.size
    pixels = imagem_pil.load()
    nova_imagem = Image.new("RGB", (largura, altura))
    novos_pixels = nova_imagem.load()
    
    offset = tamanho_janela // 2

    for x in range(offset, largura - offset):
        for y in range(offset, altura - offset):
            lista_r, lista_g, lista_b = [], [], []
            
            for i in range(-offset, offset + 1):
                for j in range(-offset, offset + 1):
                    r, g, b = pixels[x + i, y + j]
                    lista_r.append(r)
                    lista_g.append(g)
                    lista_b.append(b)
            
            lista_r.sort()
            lista_g.sort()
            lista_b.sort()
            
            meio = len(lista_r) // 2
            novos_pixels[x, y] = (lista_r[meio], lista_g[meio], lista_b[meio])
            
    return nova_imagem

def filtro_estatistico(imagem_pil, modo="minimo", tamanho_janela=3):
    largura, altura = imagem_pil.size
    pixels = imagem_pil.load()
    nova_img = Image.new("RGB", (largura, altura))
    novos_pixels = nova_img.load()
    
    offset = tamanho_janela // 2

    for x in range(offset, largura - offset):
        for y in range(offset, altura - offset):
            vizinhos_r, vizinhos_g, vizinhos_b = [], [], []
            
            for i in range(-offset, offset + 1):
                for j in range(-offset, offset + 1):
                    r, g, b = pixels[x + i, y + j]
                    vizinhos_r.append(r)
                    vizinhos_g.append(g)
                    vizinhos_b.append(b)
            
            if modo == "minimo":
                novos_pixels[x, y] = (min(vizinhos_r), min(vizinhos_g), min(vizinhos_b))
            else: # maximo
                novos_pixels[x, y] = (max(vizinhos_r), max(vizinhos_g), max(vizinhos_b))
                
    return nova_img

def filtro_gaussiano(imagem_pil, sigma=1.0):
    largura, altura = imagem_pil.size
    pixels = imagem_pil.load()
    nova_img = Image.new("RGB", (largura, altura))
    novos_pixels = nova_img.load()
    
    tamanho = 5
    offset = tamanho // 2
    kernel = [[0.0] * tamanho for _ in range(tamanho)]
    soma_kernel = 0
    
    for x in range(tamanho):
        for y in range(tamanho):
            dx = x - offset
            dy = y - offset

            exponente = -(dx**2 + dy**2) / (2 * sigma**2)
            valor = (1 / (2 * math.pi * sigma**2)) * math.exp(exponente)
            kernel[x][y] = valor
            soma_kernel += valor

    # Normaliza o kernel para que a soma dos pesos seja 1
    for i in range(tamanho):
        for j in range(tamanho):
            kernel[i][j] /= soma_kernel

    # Convolução
    for x in range(offset, largura - offset):
        for y in range(offset, altura - offset):
            r_final, g_final, b_final = 0.0, 0.0, 0.0
            
            for i in range(tamanho):
                for j in range(tamanho):
                    px_r, px_g, px_b = pixels[x + i - offset, y + j - offset]
                    peso = kernel[i][j]
                    r_final += px_r * peso
                    g_final += px_g * peso
                    b_final += px_b * peso
            
            novos_pixels[x, y] = (int(r_final), int(g_final), int(b_final))
            
    return nova_img

if __name__ == "__main__":
    try:
        img_orig = Image.open("entrada2.jpg").convert("RGB")
        
        print("Aplicando filtro da média...")
        img_media = filtro_media(img_orig, 3)
        img_media.save("resultado_media.jpg")
        
        print("Aplicando filtro da mediana...")
        img_mediana = filtro_mediana(img_orig, 3)
        img_mediana.save("resultado_mediana.jpg")
        
        print("Aplicando filtro estatístico (mínimo)...")
        img_minimo = filtro_estatistico(img_orig, modo="minimo", tamanho_janela=3)
        img_minimo.save("resultado_minimo.jpg")

        print("Aplicando filtro estatístico (máximo)...")
        img_maximo = filtro_estatistico(img_orig, modo="maximo", tamanho_janela=3)
        img_maximo.save("resultado_maximo.jpg")

        print("Aplicando filtro gaussiano...")
        img_gaussiano = filtro_gaussiano(img_orig, sigma=1.5)
        img_gaussiano.save("resultado_gaussiano.jpg")

        print("Processo concluído com sucesso!")
    except FileNotFoundError:
        print("Erro: Coloque um arquivo chamado 'entrada2.jpg' na mesma pasta.")