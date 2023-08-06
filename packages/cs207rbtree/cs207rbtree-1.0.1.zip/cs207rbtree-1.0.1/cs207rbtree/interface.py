from cs207rbtree.rbtree import RedBlackTree
from cs207rbtree.physical import Storage

class DBDB(object):

    def __init__(self, f):
        self._storage = Storage(f)
        self._tree = RedBlackTree(self._storage)

    def _assert_not_closed(self):
        if self._storage.closed:
            raise ValueError('Database closed.')

    def close(self):
        self._storage.close()

    def commit(self):
        self._assert_not_closed()
        self._tree.commit()

    def get(self, key):
        self._assert_not_closed()
        return self._tree.get(key)

    def set(self, key, value):
        self._assert_not_closed()
        return self._tree.set(key, value)

    def delete(self, key):
        self._assert_not_closed()
        return self._tree.delete(key)