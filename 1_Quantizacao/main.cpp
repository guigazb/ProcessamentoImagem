#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include "LinearQuantization.h"
#include "UniformQuantization.h"

// Função auxiliar para ler imagem PGM (formato ASCII P2)
bool readPGM(const std::string& filename, std::vector<uint8_t>& imagem, int& largura, int& altura) {
    std::ifstream arquivo(filename);
    if (!arquivo.is_open()) return false;

    std::string formato;
    arquivo >> formato;
    if (formato != "P2") return false;

    int max_val;
    arquivo >> largura >> altura >> max_val;

    imagem.resize(largura * altura);
    int pixel;
    for (int i = 0; i < largura * altura; ++i) {
        arquivo >> pixel;
        imagem[i] = static_cast<uint8_t>(pixel);
    }

    arquivo.close();
    return true;
}

// Função auxiliar para escrever imagem PGM (formato ASCII P2)
bool writePGM(const std::string& filename, const std::vector<uint8_t>& imagem, int largura, int altura) {
    std::ofstream arquivo(filename);
    if (!arquivo.is_open()) return false;

    arquivo << "P2\n";
    arquivo << largura << " " << altura << "\n";
    arquivo << "255\n"; // Valor máximo padrão

    for (int i = 0; i < largura * altura; ++i) {
        arquivo << static_cast<int>(imagem[i]) << " ";
        if ((i + 1) % largura == 0) arquivo << "\n";
    }

    arquivo.close();
    return true;
}

int main() {
    std::cout << "--- Algoritmos de Quantizacao de Imagens ---\n" << std::endl;

    std::string arquivoInput = "entrada2.pgm";
    std::vector<uint8_t> imagePixels;
    int largura = 0, altura = 0;

    // Tenta carregar a imagem
    if (!readPGM(arquivoInput, imagePixels, largura, altura)) {
        std::cerr << "Erro: Nao foi possivel abrir '" << arquivoInput << "'.\n";
        std::cerr << "Crie um arquivo 'entrada.pgm' formato P2 na mesma pasta do executavel para testar.\n";
        return 1;
    }
    
    std::cout << "Imagem carregada: " << largura << "x" << altura << " pixels.\n";

    int levels = 4; // Quantizando para 4 níveis (2 bits)

    try {
        // Quantização Uniforme
        std::cout << "Aplicando Quantizacao Uniforme (" << levels << " niveis)..." << std::endl;
        UniformQuantization uq(levels);
        std::vector<uint8_t> resultadoUniforme = uq.quantizarImagem(imagePixels);
        writePGM("saida_uniforme.pgm", resultadoUniforme, largura, altura);

        // Quantização Linear (se adapta para min/max da imagem)
        std::cout << "Aplicando Quantizacao Linear (" << levels << " niveis)..." << std::endl;
        LinearQuantization lq(levels);

        lq.fit(imagePixels); // Analisa a imagem para achar o min/max reais
        std::vector<uint8_t> resultadoLinear = lq.quantizarImagem(imagePixels);
        writePGM("saida_linear.pgm", resultadoLinear, largura, altura);
        
        std::cout << "\nProcessamento concluido! Verifique os arquivos 'saida_uniforme.pgm' e 'saida_linear.pgm'." << std::endl;

    } catch (const std::exception& e) {
        std::cerr << "Erro durante o processamento: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}