//
// MurmurHash2 http://murmurhash.googlepages.com/
// MurmurHash2, 64-bit versions, by Austin Appleby
// Note - This code makes a few assumptions about how your machine behaves -

// 1. We can read a 4-byte value from any address without crashing
// 2. sizeof(int) == 4

// And it has a few limitations -

// 1. It will not work incrementally.
// 2. It will not produce the same results on little-endian and big-endian
//    machines.
// -----------------------------------------------------------------------
// Next! Welcome to my world.
// MurmurHash2 linux python extension by Michael Lee (liyong19861014@gmail.com)
//

#include <Python.h>
#include <stdint.h>

uint32_t MurmurHash2(const void * key, uint32_t len, uint32_t seed) {
  // 'm' and 'r' are mixing constants generated offline.
  // They're not really 'magic', they just happen to work well.
  const unsigned int m = 0x5bd1e995;
  const int r = 24; 

  // Initialize the hash to a 'random' value
  unsigned int h = seed ^ len;

  // Mix 4 bytes at a time into the hash
  const unsigned char * data = (const unsigned char *)key;

  while(len >= 4) {
    unsigned int k = *(unsigned int *)data;

    k *= m;  
    k ^= k >> r;  
    k *= m;  

    h *= m;  
    h ^= k;

    data += 4;
    len -= 4;
  }

  // Handle the last few bytes of the input array
  switch(len) {
  case 3: h ^= data[2] << 16; 
  case 2: h ^= data[1] << 8;
  case 1: h ^= data[0];
    h *= m;
  };

  // Do a few final mixes of the hash to ensure the last few
  // bytes are well-incorporated.
  h ^= h >> 13;
  h *= m;
  h ^= h >> 15;
  return h;
}


uint64_t MurmurHash64B(const void * key, int len, unsigned int seed) {
  const unsigned int m = 0x5bd1e995;
  const int r = 24;

  unsigned int h1 = seed ^ len;
  unsigned int h2 = 0;

  const unsigned int * data = (const unsigned int *)key;

  while(len >= 8) {
    unsigned int k1 = *data++;
    k1 *= m; k1 ^= k1 >> r; k1 *= m;
    h1 *= m; h1 ^= k1;
    len -= 4;

    unsigned int k2 = *data++;
    k2 *= m; k2 ^= k2 >> r; k2 *= m;
    h2 *= m; h2 ^= k2;
    len -= 4;
  }

  if(len >= 4) {
    unsigned int k1 = *data++;
    k1 *= m; k1 ^= k1 >> r; k1 *= m;
    h1 *= m; h1 ^= k1;
    len -= 4;
  }

  switch(len) {
  case 3: h2 ^= ((unsigned char*)data)[2] << 16;
  case 2: h2 ^= ((unsigned char*)data)[1] << 8;
  case 1: h2 ^= ((unsigned char*)data)[0];
    h2 *= m;
  };

  h1 ^= h2 >> 18; h1 *= m;
  h2 ^= h1 >> 22; h2 *= m;
  h1 ^= h2 >> 17; h1 *= m;
  h2 ^= h1 >> 19; h2 *= m;
  uint64_t h = h1;

  h = (h << 32) | h2;
  return h;
}


static PyObject * get_unsigned_hash32(PyObject *self, PyObject *args) {
  char *key;
  unsigned len;
  unsigned seed;
  if (!PyArg_ParseTuple(args,"s#II",&key,&len,&len,&seed)) {
    return NULL;
  }
  uint32_t h = MurmurHash2(key, len, seed);
#if defined(__x86_64__)
  return PyLong_FromLong(h);
#else
  return PyLong_FromLongLong(h);
#endif
}

static PyObject * get_unsigned_hash64(PyObject *self,PyObject *args) {
  char *key;
  unsigned len;
  unsigned seed;
  if (!PyArg_ParseTuple(args,"s#II",&key,&len,&len,&seed)) {
    return NULL;
  }
  uint64_t h = MurmurHash64B(key, len, seed);
#if defined(__x86_64__)
  return PyLong_FromLong(h);
#else
  return PyLong_FromLongLong(h);
#endif

}


static PyMethodDef methods[] = {
        {"get_unsigned_hash32",(PyCFunction)get_unsigned_hash32,METH_VARARGS,NULL},
        {"get_unsigned_hash64",(PyCFunction)get_unsigned_hash64,METH_VARARGS,NULL},
        {NULL,NULL,0,NULL}
};

#if PY_MAJOR_VERSION == 2

PyMODINIT_FUNC inithash_f(void) {
        Py_InitModule3("hash_f", methods, "Google MurmurHash2 hash algorithm extension module. Feature: Unsigned version, uint32 and uint64");
}

#endif

#if PY_MAJOR_VERSION == 3
static struct PyModuleDef hash_f =
{
    PyModuleDef_HEAD_INIT,
    "hash_f", /* name of module */
    "Google MurmurHash2 hash algorithm extension module. Feature: Unsigned version, uint32 and uint64",
    -1,
    methods
};

PyMODINIT_FUNC PyInit_hash_f(void)
{
    return PyModule_Create(&hash_f);
}
#endif
