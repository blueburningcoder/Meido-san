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
    Neuron();
    virtual void getActive();
    void addToInput(double value);
    double function(double x);
};


#endif
