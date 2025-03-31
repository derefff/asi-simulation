//#include<math.h>
#include<stdlib.h>
namespace physics{

  typedef struct {
    double x;
    double y;
  } vector;

  vector* create_vector(double x, double y);
  double dot_product(vector* v1, vector* v2);
  vector* vector_add(vector* v1, vector* v2);
  vector* vector_subtract(vector* v1, vector* v2);
  vector* vector_multiply(vector* v1, vector* v2);
  vector* vector_multiply_scalar(vector* v1, double number);
}
