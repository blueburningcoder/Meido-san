#ifndef STACK_H
#define STACK_H

#include <vector>
#include <iostream>


class Stack;

class Actable {
public:
    virtual double getActive() = 0;
    virtual void Input(double) = 0;
    void setStack(Stack* own) { ownStack = own; }
    bool in_queue = false;
    Stack* ownStack = NULL;
};



class Stack : protected Actable {
protected:
    std::vector<Actable*> stack;
    int current = 0;
public:
    Stack();
    void addToStack(Actable* next);
    void workStack();
    void finishStack();
    void Input(double i) { }
    double getActive() { finishStack(); return 0; }
};


#endif
