#include "UniformQuantization.h"

UniformQuantization::UniformQuantization(int levels) : camadasQuantizacao(levels) {
    if (camadasQuantizacao < 2) camadasQuantizacao = 2; // Evita divisão por zero
}

uint8_t UniformQuantization::quantizacao(uint8_t valor) {
    // Tamanho de cada "degrau" no espaço 0-256
    float intervalo = 256.0f / camadasQuantizacao;
    
    // Descobre o índice do degrau
    int bin = static_cast<int>(valor / intervalo);
    
    // Mapeia de volta para o intervalo 0-255
    float escala = 255.0f / (camadasQuantizacao - 1);
    return static_cast<uint8_t>(bin * escala);
}

std::vector<uint8_t> UniformQuantization::quantizarImagem(const std::vector<uint8_t>& imagem) {
    std::vector<uint8_t> resultado(imagem.size());
    for (size_t i = 0; i < imagem.size(); ++i) {
        resultado[i] = quantizacao(imagem[i]);
    }
    return resultado;
}