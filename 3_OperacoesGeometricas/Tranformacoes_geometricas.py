import cv2
import numpy as np

def transformar_imagem(caminho_da_imagem):
    img = cv2.imread(caminho_da_imagem)
    if img is None:
        print("Erro ao carregar a imagem.")
        return
    
    rows, cols, ch = img.shape
    r, c = img.shape[:2]
    centro = (c // 2, r // 2)

    #TRANSLAÇÃO (Deslocamento)

    #Desloca 100 pixels para a direita e 50 para baixo
    M_trans = np.float32([[1, 0, 100], [0, 1, 50]])
    img_trans = cv2.warpAffine(img, M_trans, (cols, rows))

    #ROTAÇÃO

    #Rotaciona 45 graus em relação ao centro com escala 1.0
    centro = (cols // 2, rows // 2)
    M_rot = cv2.getRotationMatrix2D(centro, 45, 1.0)
    img_rot = cv2.warpAffine(img, M_rot, (cols, rows))

    #ESCALA (Redimensionamento)

    #Dobra o tamanho usando interpolação linear
    img_escala = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)

    #CISALHAMENTO (Shear)
    
    #Aplica uma inclinação no eixo X
    M_shear = np.float32([[1, 0.5, 0], [0, 1, 0]])
    img_shear = cv2.warpAffine(img, M_shear, (int(cols*1.5), rows))

    #REFLEXÃO (Flip)

    # 1 = Horizontal, 0 = Vertical, -1 = Ambos
    img_refl = cv2.flip(img, 1)

    #Rotação (45°) + Translação (50, 50)
    m1_rot = cv2.getRotationMatrix2D(centro, 45, 1.0)
    res1 = cv2.warpAffine(img, m1_rot, (c, r))
    m1_trans = np.float32([[1, 0, 50], [0, 1, 50]])
    res1 = cv2.warpAffine(res1, m1_trans, (c, r))

    #Cisalhamento (0.2) + Escala (0.5x)
    m2_shear = np.float32([[1, 0.2, 0], [0, 1, 0]])
    res2 = cv2.warpAffine(img, m2_shear, (int(c*1.2), r))
    res2 = cv2.resize(res2, None, fx=0.5, fy=0.5)

    #Translação (100,0) + Reflexão (H) + Rotação (90°)
    m3_trans = np.float32([[1, 0, 100], [0, 1, 0]])
    res3 = cv2.warpAffine(img, m3_trans, (c, r))
    res3 = cv2.flip(res3, 1)
    m3_rot = cv2.getRotationMatrix2D(centro, 90, 1.0)
    res3 = cv2.warpAffine(res3, m3_rot, (c, r))

    #Escala (1.2x) + Cisalhamento (0.2 Y) + Reflexão (V)
    res4 = cv2.resize(img, None, fx=1.2, fy=1.2)
    m4_shear = np.float32([[1, 0, 0], [0.2, 1, 0]])
    res4 = cv2.warpAffine(res4, m4_shear, (res4.shape[1], int(res4.shape[0]*1.2)))
    res4 = cv2.flip(res4, 0)

    #Rotação (30°) + Escala (0.7x) + Translação (-50, 20)
    m5_rot = cv2.getRotationMatrix2D(centro, 30, 0.7)
    res5 = cv2.warpAffine(img, m5_rot, (c, r))
    m5_trans = np.float32([[1, 0, -50], [0, 1, 20]])
    res5 = cv2.warpAffine(res5, m5_trans, (c, r))

    #Reflexão (Ambos eixos) + Cisalhamento (0.3) + Rotação (15°)
    res6 = cv2.flip(img, -1)
    m6_shear = np.float32([[1, 0.3, 0], [0, 1, 0]])
    res6 = cv2.warpAffine(res6, m6_shear, (int(c*1.3), r))
    m6_rot = cv2.getRotationMatrix2D(centro, 15, 1.0)
    res6 = cv2.warpAffine(res6, m6_rot, (res6.shape[1], res6.shape[0]))
   

    cv2.imshow('Original', img)
    cv2.imshow('Translacao', img_trans)
    cv2.imshow('Rotacao', img_rot)
    cv2.imshow('Escala', img_escala)
    cv2.imshow('Cisalhamento', img_shear)
    cv2.imshow('Reflexao', img_refl)
    cv2.imshow('1. Rot + Trans', res1)
    cv2.imshow('2. Shear + Escala', res2)
    cv2.imshow('3. Trans + Flip + Rot', res3)
    cv2.imshow('4. Escala + Shear + Flip', res4)
    cv2.imshow('5. Rot + Escala + Trans', res5)
    cv2.imshow('6. Flip + Shear + Rot', res6)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

transformar_imagem('daredevil-michale-lark.jpg')