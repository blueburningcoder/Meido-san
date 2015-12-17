#ifndef AXION_H
#define AXION_H

#include <iostream>
#include <vector>

#include "stack.h"


class Neuron;


class Axion : public Actable {
protected:
    std::vector<Neuron*> connected_to;
    std::vector<double> weight;
    double action = 0;
    Neuron* connection_from;
public:
    Axion(Neuron* start);
    void ConnectTo(Neuron* neuron);
    void unConnectFrom(Neuron* neuron);
    void Input(double spike);
    virtual void getActive();
};



#endif
