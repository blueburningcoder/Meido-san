#ifndef COMBINED
#define COMBINED

#include <iostream>

#include "neuron.h"
#include "axion.h"
#include "stack.h"



double Axion::getActive() {
    std::cout << "getting Axion active" << std::endl;
    double ret = input;
    std::cout << connected_to.size() << " " << weight.size() << std::endl;
    for (int i = 0; i < connected_to.size() && i < weight.size(); i++)
        connected_to[i]->Input(weight[i] * input);

    input = 0;
    in_queue = false;
    std::cout << "Axion got active" << std::endl;
    return ret;
}



double Neuron::getActive() {
    std::cout << "getting Neuron active" << std::endl;
    double sum = bias;
    for (int i = 0; i < inputStack.size(); i++)
        sum += function(inputStack[i]);
    inputStack.clear();
    connected->Input(sum + bias);
    in_queue = false;
    std::cout << "Neuron got active" << std::endl;
    return sum;
}



double OutputNeuron::getActive() {
    std::cout << "Got " << Neuron::getActive() << " as value at output " << this << std::endl;
}





#endif
