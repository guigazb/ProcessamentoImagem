#ifndef LINEAR_QUANTIZATION_H
#define LINEAR_QUANTIZATION_H

#include <vector>
#include <cstdint>

class LinearQuantization {
public:
    LinearQuantization(int levels);
    ~LinearQuantization() = default;

    void fit(const std::vector<uint8_t>& image); 
    
    uint8_t quantizacao(uint8_t value);
    std::vector<uint8_t> quantizarImagem(const std::vector<uint8_t>& image);
    
private:
    int camadasQuantizacao;
    uint8_t valorMin;
    uint8_t valorMax;
};

#endif // LINEAR_QUANTIZATION_H