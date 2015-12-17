#include "neuron.h"





Neuron::Neuron(){
    std::cout << "created Neuron" << std::endl;
}


double function(double x) {
    return x / (2 * (1 + abs(x)));
}




void Neuron::addToInput(double value) {
    inputStack.push_back(value);
    ownStack->addToStack(this);
}



