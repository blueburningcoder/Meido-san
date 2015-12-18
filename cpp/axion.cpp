#include "axion.h"





Axion::Axion(){
    std::cout << "created Axion at " << this << std::endl;
    srand((unsigned int) time(0));
}




void Axion::Input(double inp) {
    std::cout << "Inputting axion" << std::endl;
    input += inp;
    std::cout << "Adding " << this << " to stack" << std::endl;
    if (!in_queue)
        ownStack->addToStack(this);
    in_queue = true;
}



void Axion::ConnectTo(Neuron* neuron) {
    connected_to.push_back(neuron);
    weight.push_back(rand() % 5);
    std::cout << "Connected " << this << " and " << neuron << " with weight " << weight[weight.size() -1] << std::endl;
}


