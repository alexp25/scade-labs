#include "math.h"
#include "swan_types.h"

/* Exponential */
swan_float32 exp_c32_math(swan_float32 x) {
    return expf(x);
}

swan_float64 exp_c64_math(swan_float64 x) {
    return exp(x);
}

/* Power of x: x ^ k */
swan_float32 pow_c32_math(swan_float32 x, swan_int16 k) {
    return powf(x, (swan_float32)k);
}

swan_float64 pow_c64_math(swan_float64 x, swan_int16 k) {
    return pow(x, (swan_float64)k);
}


/* Square Root */
swan_float32 sqrt_c32_math(swan_float32 x) {
    return sqrtf(x);
}

swan_float64 sqrt_c64_math(swan_float64 x) {
    return sqrt(x);
}


/* Log */
swan_float32 log_c32_math(swan_float32 x) {
    return log10f(x);
}

swan_float64 log_c64_math(swan_float64 x) {
    return log10(x);
}


/* Tanh */
swan_float32 tanh_c32_math(swan_float32 x) {
    return tanhf(x);
}

swan_float64 tanh_c64_math(swan_float64 x) {
    return tanh(x);
}


/* ERF: Gaussian Error Function */
swan_float32 erf_c32_math(swan_float32 x) {
    return erff(x);
}

swan_float64 erf_c64_math(swan_float64 x) {
    return erf(x);
}
