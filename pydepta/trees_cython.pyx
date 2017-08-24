cimport cython
import numpy as np

# Cython's standard declarations
cimport cpython.mem
cimport cpython.ref
from libc cimport limits, stdio, stdlib
from libc cimport string as cstring_h   # not to be confused with stdlib 'string'
from libc.string cimport const_char

cimport lxml.includes.etreepublic as epub
from lxml.includes.tree cimport xmlNode

#from lxml.includes.tree cimport xmlDoc, xmlNode, xmlAttr, xmlNs, _isElement, _getNs

# <START> from lxml/apihelpers.pxi
cdef inline Py_ssize_t _countElements(xmlNode* c_node):
    u"Counts the elements within the following siblings and the node itself."
    cdef Py_ssize_t count
    count = 0
    while c_node is not NULL:
        if epub._isElement(c_node):
            count += 1
        c_node = c_node.next
    return count

'''
epub:
_isElement
    cdef object attributeValue(tree.xmlNode* c_element,
                               tree.xmlAttr* c_attrib_node)
    cdef tree.xmlNode* findChild(tree.xmlNode* c_node,
                                 Py_ssize_t index) nogil
    c_node.name for tag
'''

'''
def _get_root(e):
    return e.tag if e is not None else None
'''

def _get_child(e, i):
    return e[i]

def _get_children_count(e):
    #return _countElements(e._c_node.children)
    return len(e)

# inner loop from hell!
# recusive calls from 4-deep inner loop
@cython.boundscheck(False)
@cython.wraparound(False)
def tree_match(t1, t2):

    try:
        if t1.tag != t2.tag:
            return 0
    except NameError:
        return 0

    cdef int rows = _get_children_count(t1) + 1
    cdef int cols = _get_children_count(t2) + 1
    cdef int i
    cdef int j

    m = np.zeros((rows, cols), dtype=int)
    for i from 1 <= i < rows:
        for j from 1 <= j < cols:
            m[i, j] = max(m[i, j - 1],
                          m[i - 1, j],
                          m[i - 1, j - 1] + tree_match(_get_child(t1, i - 1),
                                                       _get_child(t2, j - 1)))
    return 1 + m[rows-1, cols-1]


@cython.boundscheck(False)
@cython.wraparound(False)
def create_2d_matrix(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]
