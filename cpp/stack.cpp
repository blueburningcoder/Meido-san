#include <iostream>

#define DEBUG false

#include "combined.cpp"


Stack::Stack() {
    ownStack = this;
    std::cout << "created Stack at " << this << std::endl;
}


void Stack::addToStack(Actable* next) {
    current += 1;
    stack.push_back(next);
    std::cout << "Added " << next << " to stack" << std::endl;
}



void Stack::workStack() {
    if (current >= 1 && stack.size() >= 1) {
        out("trying to do sth ... " + std::string.to_string(stack[0] ) );
        out(stack[0]->in_queue);

        stack[0]->getActive();
        stack.erase(stack.begin());
        current -= 1;
    }
}


// void Actable::getActive() { }


void Stack::finishStack() {
    while (current >= 1)
        workStack();
}


void out(std::string output) {
    if (DEBUG)
        std::cout << output << std::endl;
}


