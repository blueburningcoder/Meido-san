#include <iostream>


#include "combined.cpp"

// Main function ... not doing anything yet
int main() {
    Neuron neuron;
    Axion axion(&neuron);

    Stack stack;
    stack.addToStack(&neuron);
    stack.addToStack(&axion);

    stack.finishStack();
}
