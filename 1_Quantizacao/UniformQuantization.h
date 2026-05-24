#ifndef UNIFORM_QUANTIZATION_H
#define UNIFORM_QUANTIZATION_H

#include <vector>
#include <cstdint>

class UniformQuantization {
public:
    UniformQuantization(int levels);
    ~UniformQuantization() = default;
    
    uint8_t quantizacao(uint8_t value);
    std::vector<uint8_t> quantizarImagem(const std::vector<uint8_t>& image);
    
private:
    int camadasQuantizacao;
};

#endif // UNIFORM_QUANTIZATION_H