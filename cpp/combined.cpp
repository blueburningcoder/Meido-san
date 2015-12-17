#include "neuron.h"
#include "axion.h"



void Axion::getActive() {
    for (int i = 0; i < connected_to.size(); i++)
        connected_to[i]->addToInput(weight[i] * action);
    
    action = 0;
}



void Neuron::getActive() {
    double sum = bias;
    for (int i = 0; i < inputStack.size(); i++)
        sum += function(inputStack[i]);
    inputStack.clear();
    connected->Input(sum + bias);
}






