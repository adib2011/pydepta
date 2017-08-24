## Notes on performance

- performance varies wildly, between <0.1s and >1s
- much of time is spent in "inner loop from hell" `SimpleTreeMatcher.match`
- can we cut down on time by reusing a parsed lxml tree?
- lxml is actually using cElementTree internally...
    * https://github.com/lxml/lxml/blob/master/src/lxml/etree.pyx
    * trees are of type `_Element / _Document`
    * `_countElements(self._c_node.children)`
    * `_namespacedName(self._c_node)`


    '''
    #cdef int res
    cdef int *m = <int *>malloc(rows * cols * sizeof(int))
    try:
        for i from 1 <= i < rows:
            for j from 1 <= j < cols:
                m[i*cols + j] = max(m[i*cols + (j-1)],
                                    m[(i-1)*cols + j])
                m[i*cols + j] = max(m[i*cols + j],
                                    m[(i-1)*cols + (j-1)] +
                                    tree_match(_get_child(t1, i - 1),
                                               _get_child(t2, j - 1)))

        res = 1 + m[(rows-1)*cols + (cols-1)]
    finally:
        free(m)
        return res
    '''

