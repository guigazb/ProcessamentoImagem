#include <iostream>
#include <vector>
#include <cmath>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

//Função de saturação para garantir o limite de 8 bits
uint8_t clamp(int value) {
    if (value < 0) return 0;
    if (value > 255) return 255;
    return static_cast<uint8_t>(value);
}

//Soma (Adição de luz, efeito de dupla exposição)
void add_images(std::vector<uint8_t>& img1, const std::vector<uint8_t>& img2) {
    for (size_t i = 0; i < img1.size(); ++i) {
        img1[i] = clamp(static_cast<int>(img1[i]) + img2[i]);
    }
}

//Subtração (Ótimo para detectar diferenças ou remover fundos estáticos)
void subtract_images(std::vector<uint8_t>& img1, const std::vector<uint8_t>& img2) {
    for (size_t i = 0; i < img1.size(); ++i) {
        img1[i] = clamp(static_cast<int>(img1[i]) - img2[i]);
    }
}

//Multiplicação (Efeito "Multiply" do Photoshop - escurece usando a segunda imagem)
void multiply_images(std::vector<uint8_t>& img1, const std::vector<uint8_t>& img2) {
    for (size_t i = 0; i < img1.size(); ++i) {
        // A matemática correta: (A * B) / 255
        // Isso simula a conversão para 0.0 - 1.0 sem precisar usar floats lentos
        int mul = (static_cast<int>(img1[i]) * img2[i]) / 255;
        img1[i] = clamp(mul);
    }
}

//Divisão (Efeito "Divide" - clareia usando a segunda imagem)
void divide_images(std::vector<uint8_t>& img1, const std::vector<uint8_t>& img2) {
    for (size_t i = 0; i < img1.size(); ++i) {
        if (img2[i] == 0) {
            //Se o divisor for preto (0), o resultado tende ao infinito (branco máximo)
            img1[i] = 255;
        } else {
            //A matemática correta: (A * 255) / B
            int div = (static_cast<int>(img1[i]) * 255) / img2[i];
            img1[i] = clamp(div);
        }
    }
}

int main() {
    std::cout << "Laboratorio: Operacoes entre Duas Imagens\n" << std::endl;

    const char* file1 = "entrada.jpeg";
    const char* file2 = "entrada.jpeg";

    int w1, h1, c1;
    int w2, h2, c2;

    unsigned char* data1 = stbi_load(file1, &w1, &h1, &c1, 0);
    if (!data1) {
        std::cerr << "Erro ao carregar " << file1 << std::endl;
        return 1;
    }

    unsigned char* data2 = stbi_load(file2, &w2, &h2, &c2, 0);
    if (!data2) {
        std::cerr << "Erro ao carregar " << file2 << std::endl;
        stbi_image_free(data1);
        return 1;
    }

    if (w1 != w2 || h1 != h2 || c1 != c2) {
        std::cerr << "Erro Crítico: As imagens possuem tamanhos ou canais diferentes!" << std::endl;
        std::cerr << "Img1: " << w1 << "x" << h1 << " (" << c1 << " canais)" << std::endl;
        std::cerr << "Img2: " << w2 << "x" << h2 << " (" << c2 << " canais)" << std::endl;
        stbi_image_free(data1);
        stbi_image_free(data2);
        return 1;
    }

    std::cout << "Imagens compativeis: " << w1 << "x" << h1 << std::endl;

    size_t total_bytes = w1 * h1 * c1;
    std::vector<uint8_t> base_img1(data1, data1 + total_bytes);
    std::vector<uint8_t> base_img2(data2, data2 + total_bytes);

    stbi_image_free(data1);
    stbi_image_free(data2);
    
    std::vector<uint8_t> img_soma = base_img1;
    add_images(img_soma, base_img2);
    stbi_write_jpg("resultado_soma.jpg", w1, h1, c1, img_soma.data(), 100);
    std::cout << "Soma concluida: 'resultado_soma.jpg'" << std::endl;

    std::vector<uint8_t> img_subtracao = base_img1;
    subtract_images(img_subtracao, base_img2);
    stbi_write_jpg("resultado_subtracao.jpg", w1, h1, c1, img_subtracao.data(), 100);
    std::cout << "Subtracao concluida: 'resultado_subtracao.jpg'" << std::endl;

    std::vector<uint8_t> img_multiplicacao = base_img1;
    multiply_images(img_multiplicacao, base_img2);
    stbi_write_jpg("resultado_multiplicacao.jpg", w1, h1, c1, img_multiplicacao.data(), 100);
    std::cout << "Multiplicacao concluida: 'resultado_multiplicacao.jpg'" << std::endl;

    std::vector<uint8_t> img_divisao = base_img1;
    divide_images(img_divisao, base_img2);
    stbi_write_jpg("resultado_divisao.jpg", w1, h1, c1, img_divisao.data(), 100);
    std::cout << "Divisao concluida: 'resultado_divisao.jpg'" << std::endl;

    return 0;
}