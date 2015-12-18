#include <iostream>


#include "import_all.h"

// Main function ... not doing anything real just yet
int main() {
    Axion axion, axion1;
    OutputNeuron out(&axion1);
    Neuron neuron(&axion);

    axion.ConnectTo(&out);

    Stack stack;

    neuron.setStack(&stack);
    axion.setStack(&stack);
    out.setStack(&stack);
    axion1.setStack(&stack);

    neuron.Input(3);

    stack.finishStack();

    return 0;
}


