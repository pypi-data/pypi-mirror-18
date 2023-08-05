// -*- C++ -*-
// IVec.h: Integer version of the 3-vector class in Vec.h
//
// Copyright (C) 2008-2011 Jakob Schiotz and Center for Individual
// Nanoparticle Functionality, Department of Physics, Technical
// University of Denmark.  Email: schiotz@fysik.dtu.dk
//
// This file is part of Asap version 3.
// Asap is released under the GNU Lesser Public License (LGPL) version 3.
// However, the parts of Asap distributed within the OpenKIM project
// (including this file) are also released under the Common Development
// and Distribution License (CDDL) version 1.0.
//
// This program is free software: you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public License
// version 3 as published by the Free Software Foundation.  Permission
// to use other versions of the GNU Lesser General Public License may
// granted by Jakob Schiotz or the head of department of the
// Department of Physics, Technical University of Denmark, as
// described in section 14 of the GNU General Public License.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// and the GNU Lesser Public License along with this program.  If not,
// see <http://www.gnu.org/licenses/>.


#ifndef __IVEC_H__
#define __IVEC_H__

#include <iostream>
using std::istream;
using std::ostream;

namespace ASAPSPACE {

/// An integer 3-vector.

/// The only data is the three positions (and there are no virtual
/// functions), so the memory layout of an array of IVecs will be x0,
/// y0, z0, x1, y1, z1, x2, ...
///
/// Almost all operations are inline for speed.

class IVec
{
public:
  /// Dummy constructor needed by STL containers.
  IVec() {};
  /// Construct a 3-vector from three ints.
  IVec(int x0, int x1, int x2);
  /// Dot product
  int operator*(const IVec& v) const;
  /// Multiplication with scalar
  IVec operator*(const int& s) const;
  /// Add two IVecs
  IVec operator+(const IVec& v) const;
  /// Subtract two IVecs
  IVec operator-(const IVec& v) const;
  /// Unary minus
  IVec operator-() const;
  /// Add a IVec to this one.
  IVec& operator+=(const IVec& v);
  /// Subtract a vec from this one.
  IVec& operator-=(const IVec& v);
  /// Multiply this vec with a scalar
  IVec& operator*=(int s);
  /// Divide this IVec with a scalar.
  IVec& operator/=(int s);
  /// IVec equality
  bool operator==(const IVec &v) const;
  /// const indexing
  int operator[](int n) const;
  /// Non-const indexing
  int& operator[](int n);
  /// Cross product of two IVecs.
  friend IVec Cross(const IVec& v1, const IVec& v2);
  /// The length of a IVec
  friend int Length2(const IVec& v);
  /// Increment y with a times x.
  friend void Vaxpy(int a, const IVec& x, IVec& y);
  /// Print a Vec
  friend ostream& operator<<(ostream& out, const Vec& v);
public:
  int x, y, z;
};

inline IVec::IVec(int x0, int x1, int x2)
{
  x = x0;
  y = x1;
  z = x2;
}

inline int IVec::operator*(const IVec& v) const
{
  return x * v.x + y * v.y + z * v.z;
}

inline IVec IVec::operator*(const int& s) const
{
  return IVec(s * x, s * y, s * z);
}

inline IVec IVec::operator+(const IVec& v) const
{
  return IVec(x + v.x, y + v.y, z + v.z);
}

inline IVec IVec::operator-(const IVec& v) const
{
  return IVec(x - v.x, y - v.y, z - v.z);
}

inline IVec IVec::operator-() const
{
  return IVec(-x, -y, -z);
}

inline IVec& IVec::operator+=(const IVec& v)
{
  x += v.x; y += v.y; z += v.z;
  return *this;
}

inline IVec& IVec::operator-=(const IVec& v)
{
  x -= v.x; y -= v.y; z -= v.z;
  return *this;
}

inline IVec& IVec::operator*=(int s)
{
  x *= s; y *= s; z *= s;
  return *this;
}

inline IVec& IVec::operator/=(int s)
{
  x /= s; y /= s; z /= s;
  return *this;
}

inline bool IVec::operator==(const IVec &v) const
{
  return (x == v.x) && (y == v.y) && (z == v.z);
}

inline int IVec::operator[](int n) const
{
  return (&x)[n];
}

inline int& IVec::operator[](int n)
{
  return (&x)[n];
}

inline IVec Cross(const IVec& v1, const IVec& v2)
{
  return IVec(v1.y * v2.z - v1.z * v2.y,
             v1.z * v2.x - v1.x * v2.z,
             v1.x * v2.y - v1.y * v2.x);
}

inline void Vaxpy(int a, const IVec& x, IVec& y)
{
  y.x += a * x.x;
  y.y += a * x.y;
  y.z += a * x.z;
}

inline int Length2(const IVec& v)
{
  return v.x * v.x + v.y * v.y + v.z * v.z;
}

inline ostream& operator<<(ostream& out, const IVec& v)
{
  out << "(" << v.x << ", " << v.y << ", " << v.z << ")";
  return out;
}

} // end namespace

#endif // __IVEC_H__

