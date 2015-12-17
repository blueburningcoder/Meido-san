#include "stack.h"


void Stack::addToStack(Actable* next) {
    current += 1;
    stack.push_back(next);
}



void Stack::workStack() {
    if (current >= 1) {
        stack[0]->getActive();
        stack.erase(stack.begin());
        current -= 1;
    }
}



void Stack::finishStack() {
    while (current >= 1)
        workStack();
}


