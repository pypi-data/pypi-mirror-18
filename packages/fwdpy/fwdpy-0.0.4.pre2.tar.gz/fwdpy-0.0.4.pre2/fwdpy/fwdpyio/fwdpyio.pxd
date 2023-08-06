from libcpp.string cimport string
from fwdpy.fwdpy cimport *

cdef extern from "fwdpyio_serialize.hpp" namespace "fwdpy::serialize" nogil:
    string serialize_singlepop(const singlepop_t * pop)
    vector[shared_ptr[singlepop_t]] deserialize_singlepop(const vector[string] & strings)
    string serialize_metapop(const metapop_t * pop)
    vector[shared_ptr[metapop_t]] deserialize_metapop(const vector[string] & strings)
    string serialize_multilocus(const multilocus_t * pop)
    vector[shared_ptr[multilocus_t]] deserialize_multilocus(const vector[string] & strings)

