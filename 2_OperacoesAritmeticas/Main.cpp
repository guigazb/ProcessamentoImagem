#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>

// Implementação das bibliotecas STB para leitura e escrita de JPEG
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

// Função de saturação para garantir pixel 8 bits
uint8_t clamp(int value) {
    if (value < 0) return 0;
    if (value > 255) return 255;
    return static_cast<uint8_t>(value);
}

// 1. Soma (Clarear a imagem)
void image_add(std::vector<uint8_t>& image, int scalar) {
    for (size_t i = 0; i < image.size(); ++i) {
        // Converte para int, soma, aplica o clamp e devolve como uint8_t
        image[i] = clamp(static_cast<int>(image[i]) + scalar);
    }
}

// 2. Subtração (Escurecer a imagem)
void image_subtract(std::vector<uint8_t>& image, int scalar) {
    for (size_t i = 0; i < image.size(); ++i) {
        image[i] = clamp(static_cast<int>(image[i]) - scalar);
    }
}

// 3. Multiplicação (Aumentar o contraste)
void image_multiply(std::vector<uint8_t>& image, float scalar) {
    for (size_t i = 0; i < image.size(); ++i) {
        image[i] = clamp(static_cast<int>(std::round(image[i] * scalar)));
    }
}

// 4. Divisão (Diminuir o contraste)
void image_divide(std::vector<uint8_t>& image, float scalar) {
    if (scalar == 0.0f) {
        std::cerr << "Erro matemático: Divisão por zero não permitida!" << std::endl;
        return;
    }
    for (size_t i = 0; i < image.size(); ++i) {
        image[i] = clamp(static_cast<int>(std::round(image[i] / scalar)));
    }
}

int main() {
    std::cout << "Laboratorio de Aritmetica de Imagens\n" << std::endl;

    const char* entrada = "entrada.jpeg";
    int largura, altura, canais;

    // Passamos 0 no final para pedir à biblioteca manter o número original de canais (ex: 3 para RGB)
    unsigned char* img_data = stbi_load(entrada, &largura, &altura, &canais, 0);
    
    if (img_data == nullptr) {
        std::cerr << "Erro: Nao foi possivel carregar a imagem '" << entrada << "'." << std::endl;
        return 1;
    }

    std::cout << "Imagem carregada: " << largura << "x" << altura << " (" << canais << " canais de cor)" << std::endl;

    // Transferimos os dados crus para um std::vector seguro e gerenciável
    size_t total_bytes = largura * altura * canais;
    std::vector<uint8_t> pixels(img_data, img_data + total_bytes);
    
    // Liberamos a memória alocada pelo C puro do stb_image
    stbi_image_free(img_data);

    // Fazemos uma cópia do vetor original para cada operação não sobrepor a outra    
    std::vector<uint8_t> img_soma = pixels;
    image_add(img_soma, 50); // Soma 50 a todos os pixels
    stbi_write_jpg("saida_soma.jpg", largura, altura, canais, img_soma.data(), 100); // 100 é a qualidade do JPEG
    std::cout << "Imagem clareada salva como 'saida_soma.jpg'." << std::endl;

    std::vector<uint8_t> img_subtracao = pixels;
    image_subtract(img_subtracao, 50); // Subtrai 50 de todos os pixels
    stbi_write_jpg("saida_subtracao.jpg", largura, altura, canais, img_subtracao.data(), 100);
    std::cout << "Imagem escurecida salva como 'saida_subtracao.jpg'." << std::endl;

    std::vector<uint8_t> img_multiplicacao = pixels;
    image_multiply(img_multiplicacao, 1.5f); // Aumenta os valores em 50%
    stbi_write_jpg("saida_multiplicacao.jpg", largura, altura, canais, img_multiplicacao.data(), 100);
    std::cout << "Imagem com brilho/contraste multiplicado salva como 'saida_multiplicacao.jpg'." << std::endl;

    std::vector<uint8_t> img_divisao = pixels;
    image_divide(img_divisao, 2.0f); // Corta os valores pela metade
    stbi_write_jpg("saida_divisao.jpg", largura, altura, canais, img_divisao.data(), 100);
    std::cout << "Imagem com brilho/contraste dividido salva como 'saida_divisao.jpg'." << std::endl;

    std::cout << "\nOperacoes concluidas com sucesso!" << std::endl;

    return 0;
}