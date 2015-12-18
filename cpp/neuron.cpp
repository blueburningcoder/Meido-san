#include "neuron.h"





Neuron::Neuron(Axion* connection){
    connected = connection;
    std::cout << "created Neuron at " << this << std::endl;
}


double Neuron::function(double x) {
    return x / (2 * (1 + abs(x)));
}



void Neuron::Input(double value) {
    inputStack.push_back(value);
    if (!in_queue)
        ownStack->addToStack(this);
    in_queue = true;
}



OutputNeuron::OutputNeuron(Axion* connection) : Neuron(connection) {
    std::cout << "created OutputNeuron at " << this << std::endl;
}

