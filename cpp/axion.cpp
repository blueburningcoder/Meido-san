#include "axion.h"





Axion::Axion(Neuron* start){
    connection_from = start;
    std::cout << "created Axion" << std::endl;
}




void Axion::Input(double value) {
    action = value;
    ownStack->addToStack(this);
}


