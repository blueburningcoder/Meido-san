/*
Introspections in other languages 


are typetraits in c++





If you have a template,  ...

templates are only 'generated' when needed -> lazy











other C++ stuff I definitely need to look at:
typedef, typedecl, namespace, templates, traits, 'using', threads (again!) 

template-specialisation based on type-traits
*/




template <int Val>
struct Foo {
    enum {value = Val};
    static constexpr double const invval  = 1./Val;
};


static_assert(Foo<2>::invval == .5, "foobar");


namespace unit {

typedef unsigned long long uint;

template <uint Lhs, uint Rhs>
struct euclid : euclid<Rhs, Lhs % Rhs> {};


template <uint Gcd>
struct euclid<Gcd, 0> { static constexpr uint const value{Gcd}; };

constexpr uint gcd(uint const a, uint const b) {
    return b == 0 ? a : gcd (b, a % b);
}

template <uint Num, uint Denom>


struct rational {
    static_assert(Denom != 0, "No 0 denominator allowed!");
    static constexpr uint const numerator{Num};
    static constexpr uint const denominator{Num};
    typedef rational<numerator, denominator> minimal;
};

static_assert(rational<2,3>::denominator == 2, "foobar");

static_assert(rational<2,10>::numerator == rational<2,4>::numerator, "foobar");
static_assert(rational<5,10>::denominator == rational<5,10>::denominator, "foobar");
// static_assert(rational<5,10>::denominator == rational<2,10>::denominator, "foobar"); // for some reason fails becauso of the two not being a five


template <class Op>
struct rational_unary {
    typedef rational<Op::denominator, Op::numerator> invert;
};

template <class Op>
using rational_invert_t = typename rational_unary<Op>::invert;

template <class Lhs, class Rhs>
struct rational_binary {
    static_assert(Lhs::numerator * Rhs::numerator / Rhs::numerator == Lhs::numerator, "Overflow in numerator multiplication!");
    static_assert(Lhs::denominator * Rhs::denominator / Rhs::denominator == Lhs::denominator, "Overflow in denominator multiplication!");
    typedef rational<Lhs::numerator * Rhs::numerator, Lhs::denominator * Rhs::denominator> mul;
};

template <class Op>
using rational_minimal_t = typename Op::minimal;

template <class Lhs, class Rhs>
using rational_mul_t = typename rational_binary<Lhs, Rhs>::mul;

template <class Lhs, class Rhs>
using rational_div_t = rational_mul_t<Lhs, rational_invert_t<Rhs>>;

// Template specification
template <class A, class B>
struct is_same { static constexpr bool value{false}; };

template <class A>
struct is_same <A, A> { static constexpr bool value{true}; };

static_assert(rational_mul_t<rational<1,2>, rational<23,1>>::numerator == 23, "foooobar");

static_assert(is_same<rational_mul_t<rational<1,2>, rational<2,1>>, rational<2,2>>::value, "equalisation");


typedef long long sint;

template <sint Exponent, class Tail = void>
struct exponents_chain {
    typedef Tail tail;
    static constexpr sint const value{exponents};
};

template <sint Exponent, sint... Tail>
struct exponents<Exponent, Tail...> {
    typedef exponents_chain<Exponent, typename exponents<Tail...>::type> type;
};

template <sint... Exponent>
struct exponents { typedef void type; };

template <sint... Exponents>
using exponents_t = typename exponents<Exponents...>::type;

template <class Op>
struct exponents_unary {
    typedef exponents_chain<-Op::value, typename exponents_unary<typename Op::tail>::negate> negate;
};

template <>
struct exponents_unary {
    typedef void negate;
};

template <class Op>
using exponents_negate_t = typename exponents_unary<Op>::negate;

template <class Lhs, class Rhs>
struct exponents_binary {
    typedef exponents_chain<Lhs::value + Rhs::value, typename exponents_binary<typename Lhs::tail, typename Rhs::tail>::add> add;
};

template <> 
struct exponents_binary<void, void> {
    typedef void add;
};

template <class Lhs, class Rhs>
using exponents_add_t = exponents_add_t<Lhs, exponents_negate_t<Rhs>>;

template <class Lhs, class Rhs>
using exponents_sub_t = exponents_add_t<Lhs, exponents_negate_t<Rhs>>;


static_assert(is_same<exponents_t<1, -2, 0>, exponents_add_t<exponents_t<2,3,2>, exponents_t<-1,-5,-2>>>::value, "foobar");

template <class ...>
using void_t = void;



#include <type_traits>
using std::false_type
using std::true_type


template <typename T>
struct foo {
    template <class X = T, class = void_t<decltype(X::value)>>
    void foo(X bar) {};
};


template <class Op>
using exponents_negate_t = typename exponents_unary<Op>::negate;

template <class Lhs, class Rhs, class = void>
struct is_same_length : false_type {};

template <class Lhs, class Rhs>
struct is_same_length<Lhs, Rhs, void_t<typename Lhs::tail, typename Rhs::tail>>
    : is_same_length<typename Lhs::tail, typename Rhs::tail> {};

template <>
struct is_same_length<void,void> : true_type {};


// SFINAE



}

int main() {}

