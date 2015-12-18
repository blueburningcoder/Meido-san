#ifndef AXION_H
#define AXION_H

#include <iostream>
#include <vector>
#include <ctime>

#include "stack.h"


class Neuron;


class Axion : public Actable {
protected:
    std::vector<Neuron*> connected_to;
    std::vector<double> weight;
    double input = 0;
public:
    Axion();
    void ConnectTo(Neuron* neuron);
    void unConnectFrom(Neuron* neuron);
    void Input(double inp);
    double getActive();
};



#endif
