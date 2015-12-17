#ifndef STACK_H
#define STACK_H

#include <vector>
#include <iostream>


class Stack;

class Actable {
public:
    virtual void getActive()=0;
    static Stack* ownStack;
};



class Stack : public Actable {
protected:
    std::vector<Actable*> stack;
    int current = 0;
public:
    Stack() { ownStack = this; }
    void addToStack(Actable* next);
    void workStack();
    void finishStack();
    virtual void getActive() { finishStack(); }
};


#endif
