import cv2
import numpy as np
import os
import pandas as pd
import glob

# ==========================================
# CONFIGURAÇÕES DE DIRETÓRIO
# ==========================================
INPUT_DIR = './dataset/archive/images_gz2/images'      
OUTPUT_IMG_DIR = './dataset/output' 
OUTPUT_CSV = './galaxy_features.csv'  # Onde os atributos CAS serão salvos
os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)

# FUNÇÕES DE CÁLCULO DOS ÍNDICES CAS
def calcular_assimetria(img, mascara, cx, cy):
    """ Calcula a Assimetria (A) rotacionando a imagem em 180 graus. """
    # Cria matriz de rotação
    matriz_rot = cv2.getRotationMatrix2D((cx, cy), 180, 1.0)
    img_rotacionada = cv2.warpAffine(img, matriz_rot, (img.shape[1], img.shape[0]))
    
    # Aplica a fórmula A = sum(|I - I_180|) / (2 * sum(|I|)) apenas na área da galáxia
    diferenca = cv2.absdiff(img, img_rotacionada)
    
    soma_diff = np.sum(diferenca[mascara == 255])
    soma_img = np.sum(img[mascara == 255])
    
    # Evita divisão por zero
    if soma_img == 0: return 0
    return soma_diff / (2.0 * soma_img)

def calcular_suavidade(img, mascara):
    """ Calcula a Suavidade (S) comparando a imagem com uma versão borrada. """
    # Borra a imagem para remover texturas finas
    img_suave = cv2.GaussianBlur(img, (15, 15), 0)
    
    diferenca = cv2.absdiff(img, img_suave)
    
    soma_diff = np.sum(diferenca[mascara == 255])
    soma_img = np.sum(img[mascara == 255])
    
    if soma_img == 0: return 0
    return soma_diff / soma_img

def calcular_concentracao(img, mascara, cx, cy):
    """ Calcula a Concentração (C) baseada na luz no núcleo vs periferia. """
    # Aproximação para Visão Computacional: Luz no raio central (30% da galáxia) 
    # vs Luz total da galáxia.
    
    # Encontra os contornos da máscara para achar o raio aproximado da galáxia
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos: return 0
    
    maior_contorno = max(contornos, key=cv2.contourArea)
    _, raio = cv2.minEnclosingCircle(maior_contorno)
    
    # Cria uma máscara apenas para o núcleo (raio / 3)
    mascara_nucleo = np.zeros_like(mascara)
    cv2.circle(mascara_nucleo, (int(cx), int(cy)), int(raio/3), 255, -1)
    
    luz_nucleo = np.sum(img[mascara_nucleo == 255])
    luz_total = np.sum(img[mascara == 255])
    
    if luz_total == 0: return 0
    return luz_nucleo / luz_total

# ==========================================
# PIPELINE PRINCIPAL DE PROCESSAMENTO
# ==========================================
def processar_imagem(caminho_img):
    # 1. Carrega a imagem em escala de cinza
    img = cv2.imread(caminho_img, cv2.IMREAD_GRAYSCALE)
    if img is None: return None
    
    # 2. Denoising (Remoção de ruído sal e pimenta do espaço)
    img_filtrada = cv2.medianBlur(img, 5)
    
    # 3. Realce de Contraste (CLAHE) para revelar braços espirais
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img_realcada = clahe.apply(img_filtrada)
    
    # 4. Segmentação (Isolar a galáxia do fundo)
    _, limiar = cv2.threshold(img_realcada, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Operações Morfológicas para limpar a máscara (Abertura e Fechamento)
    kernel = np.ones((5,5), np.uint8)
    mascara = cv2.morphologyEx(limiar, cv2.MORPH_OPEN, kernel)
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)
    
    # 5. Encontrar o Centro da Galáxia (Momentos Espaciais)
    M = cv2.moments(mascara)
    if M["m00"] == 0: # Previne divisão por zero se a máscara for vazia
        return None
    
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    
    # 6. Extrair Atributos CAS
    A = calcular_assimetria(img_realcada, mascara, cx, cy)
    S = calcular_suavidade(img_realcada, mascara)
    C = calcular_concentracao(img_realcada, mascara, cx, cy)
    
    # 7. Isolar o fundo (opcional, deixa o fundo totalmente preto)
    img_final = cv2.bitwise_and(img_realcada, img_realcada, mask=mascara)
    
    return img_final, A, C, S

# ==========================================
# EXECUÇÃO EM LOTE
# ==========================================
def main():
    lista_imagens = glob.glob(os.path.join(INPUT_DIR, '*.jpg')) # Adapte a extensão se for .jpeg ou .png
    dados_features = []
    
    print(f"Iniciando o processamento de {len(lista_imagens)} imagens...")
    
    for idx, caminho_img in enumerate(lista_imagens):
        nome_arquivo = os.path.basename(caminho_img)
        
        resultado = processar_imagem(caminho_img)
        if resultado is None:
            print(f"Erro ao processar: {nome_arquivo}")
            continue
            
        img_final, A, C, S = resultado
        
        # Salva a imagem tratada
        caminho_saida = os.path.join(OUTPUT_IMG_DIR, nome_arquivo)
        cv2.imwrite(caminho_saida, img_final)
        
        # Guarda as features
        dados_features.append({
            'galaxy_id': nome_arquivo.split('.')[0],
            'Asymmetry': A,
            'Concentration': C,
            'Smoothness': S
        })
        
        if idx % 100 == 0 and idx > 0:
            print(f"{idx} imagens processadas...")
            
    # Salva o DataFrame como CSV
    df_features = pd.DataFrame(dados_features)
    df_features.to_csv(OUTPUT_CSV, index=False)
    print(f"Processamento concluído! Features salvas em {OUTPUT_CSV}")

if __name__ == '__main__':
    main()