#ifndef NEURON_H
#define NEURON_H

#include <iostream>
#include <vector>

#include "stack.h"


class Axion;


class Neuron : public Actable {
protected:
    Axion* connected;
    std::vector<double> inputStack;
    double bias = 0;
public:
    Neuron(Axion* connection);
    double function(double x);
    void Input(double);
    double getActive();
};



class OutputNeuron : public Neuron {
public:
    OutputNeuron(Axion* connection);
    double getActive();
    void Input(double d) { Neuron::Input(d); }
};


#endif
