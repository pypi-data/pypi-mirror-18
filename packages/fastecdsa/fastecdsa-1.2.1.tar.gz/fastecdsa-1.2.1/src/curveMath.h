#ifndef CURVEMATH_H
#define CURVEMATH_H

#include <Python.h>

#include <gmp.h>
#include "curve.h"
#include "point.h"

int pointEqual(const Point * pointA, const Point * pointB);
void pointDouble(const Point * pointP, Point * pointR, Curve * curve);
void pointAdd(const Point * pointP, const Point * pointQ, Point * pointR, Curve * curve);
void pointMul(const Point * pointP, Point * pointR, const mpz_t d, Curve * curve);

#endif
