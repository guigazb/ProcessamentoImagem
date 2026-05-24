#include "LinearQuantization.h"
#include <algorithm>

LinearQuantization::LinearQuantization(int camadas) : camadasQuantizacao(camadas), valorMin(0), valorMax(255) {
    if (camadasQuantizacao < 2) camadasQuantizacao = 2;
}

void LinearQuantization::fit(const std::vector<uint8_t>& imagem) {
    if (imagem.empty()) return;
    
    valorMin = imagem[0];
    valorMax = imagem[0];
    
    for (uint8_t pixel : imagem) {
        if (pixel < valorMin) valorMin = pixel;
        if (pixel > valorMax) valorMax = pixel;
    }
    
    if (valorMin == valorMax) valorMax = valorMin + 1; // Evita divisão por zero se a imagem for de uma cor só
}

uint8_t LinearQuantization::quantizacao(uint8_t value) {
    if (value <= valorMin) return 0;
    if (value >= valorMax) return 255;
    
    // Normaliza o pixel para um valor entre 0.0 e 1.0 com base no min e max da imagem
    float normalizado = static_cast<float>(value - valorMin) / (valorMax - valorMin);
    
    // Encontra o bin
    int bin = static_cast<int>(normalizado * camadasQuantizacao);
    if (bin >= camadasQuantizacao) bin = camadasQuantizacao - 1;
    
    // Mapeia para 0-255
    float scale = 255.0f / (camadasQuantizacao - 1);
    return static_cast<uint8_t>(bin * scale);
}

std::vector<uint8_t> LinearQuantization::quantizarImagem(const std::vector<uint8_t>& imagem) {
    std::vector<uint8_t> result(imagem.size());
    for (size_t i = 0; i < imagem.size(); ++i) {
        result[i] = quantizacao(imagem[i]);
    }
    return result;
}