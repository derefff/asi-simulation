#include "vector.h"

namespace physics{

  vector* create_vector(double x, double y)
  {
    vector* vec = (vector*)malloc(sizeof(vector));
    vec->x = x;
    vec->y = y;
    return vec;
  }


  double dot_product(vector* v1, vector* v2) {
    return v1->x * v2->x + v1->y * v2->y;
}

vector* vector_add(vector* v1, vector* v2) {
    vector* result = create_vector(v1->x + v2->x, v1->y + v2->y);
    return result;
}

vector* vector_subtract(vector* v1, vector* v2) {
    vector* result = create_vector(v1->x - v2->x, v1->y - v2->y);
    return result;
}

vector* vector_multiply(vector* v1, vector* v2) {
    vector* result = create_vector(v1->x * v2->x, v1->y * v2->y);
    return result;
}

vector* vector_multiply_scalar(vector* v1, double number) {
    vector* result = create_vector(v1->x * number, v1->y * number);
    return result;
}
}