import pickle

from logical import ValueRef

class Color:
    RED = 0
    BLACK = 1

class RedBlackNodeRef(ValueRef):
    """Reference to a btree node on disk
    """
    
    #calls the RedBlackNode's store_refs
    def prepare_to_store(self, storage):
        """Have a node store its refs
        """
        if self._referent:
            self._referent.store_refs(storage)

    @staticmethod
    def referent_to_bytes(referent):
        """Use pickle to convert node to bytes
        """
        return pickle.dumps({
            'left': referent.left_ref.address,
            'key': referent.key,
            'value': referent.value_ref.address,
            'right': referent.right_ref.address,
            'color': referent.color
        })

    @staticmethod
    def bytes_to_referent(string):
        """Unpickle bytes to get a node object
        """
        d = pickle.loads(string)
        return RedBlackNode(
            RedBlackNodeRef(address=d['left']),
            d['key'],
            ValueRef(address=d['value']),
            RedBlackNodeRef(address=d['right']),
            d['color']
        )


class RedBlackNode:

    def __init__(self, left_ref, key, value_ref, right_ref, color):
        self.left_ref = left_ref
        self.key = key
        self.value_ref = value_ref
        self.right_ref = right_ref
        self.color = color

    @classmethod
    def from_node(cls, node, **kwargs):
        """Clone a node with some changes from another one
        """
        return cls(
            left_ref=kwargs.get('left_ref', node.left_ref),
            key=kwargs.get('key', node.key),
            value_ref=kwargs.get('value_ref', node.value_ref),
            right_ref=kwargs.get('right_ref', node.right_ref),
            color=kwargs.get('color', node.color)
        )

    def store_refs(self, storage):
        """Method for a node to store all of its stuff
        """
        self.value_ref.store(storage)
        #calls BinaryNodeRef.store. which calls BinaryNodeRef.prepate_to_store
        #which calls this again and recursively stores the whole tree
        self.left_ref.store(storage)
        self.right_ref.store(storage)

    def blacken(self):
        if self.is_red():
            return self.from_node(
                self,
                color=Color.BLACK,
            )
        return self

    # def is_empty(self):
    #     return False

    def is_black(self):
        return self.color == Color.BLACK

    def is_red(self):
        return self.color == Color.RED


class RedBlackTree:

    def __init__(self, storage):
        self._storage = storage
        self._refresh_tree_ref()

    def commit(self):
        "changes are final only when committed"
        #triggers BinaryNodeRef.store
        self._tree_ref.store(self._storage)
        #make sure address of new tree is stored
        self._storage.commit_root_address(self._tree_ref.address)

    def _refresh_tree_ref(self):
        "get reference to new tree if it has changed"
        self._tree_ref = RedBlackNodeRef(
            address=self._storage.get_root_address())

    # @property
    # def color(self):
    #     return self.color

    # @property
    # def value(self):
    #     return self.value

    # @property
    # def right(self):
    #     return self.right

    # @property
    # def left(self):
    #     return self._left
    def get(self, key):
        """Get value for a key
        """
        #if tree is not locked by another writer
        #refresh the references and get new tree if needed
        if not self._storage.locked:
            self._refresh_tree_ref()
        #get the top level node
        node = self._follow(self._tree_ref)
        #traverse until you find appropriate node
        while node is not None:
            if key < node.key:
                node = self._follow(node.left_ref)
            elif key > node.key:
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
        raise KeyError
    
    def set(self, key, value):
        """Set a new value in the tree. will cause a new tree
        """
        #try to lock the tree. If we succeed make sure
        #we dont lose updates from any other process
        if self._storage.lock():
            self._refresh_tree_ref()
        #get current top-level node and make a value-ref
        node = self._follow(self._tree_ref)
        value_ref = ValueRef(value)
        #insert and get new tree ref
        self._tree_ref = self._insert(node, key, value_ref)

    def update(self, node, key, value_ref):
        if node is None:
            new_node = RedBlackNode(
                RedBlackNodeRef(), key, value_ref, RedBlackNodeRef(), Color.RED)
        elif key < node.key:
            new_node = RedBlackNode.from_node(
                node,
                left_ref=self.update(
                    self._follow(node.left_ref), key, value_ref))
        elif node.key < key:
            new_node = RedBlackNode.from_node(
                node,
                right_ref=self.update(
                    self._follow(node.right_ref), key, value_ref))
        else:
            new_node = RedBlackNode.from_node(node, value_ref=value_ref)
        new_node = self.balance(new_node)
        return RedBlackNodeRef(referent=new_node)

    def _insert(self, node, key, value_ref):
        new_node = self._follow(self.update(node, key, value_ref))
        return RedBlackNodeRef(referent=new_node.blacken())

    def rotate_left(self, node):
        return RedBlackNode(
            left_ref=RedBlackNodeRef(
                referent=RedBlackNode.from_node(
                    node,
                    right_ref=self._follow(node.right_ref).left_ref
                )
            ),
            key=self._follow(node.right_ref).key,
            value_ref=self._follow(node.right_ref).value_ref,
            right_ref=self._follow(node.right_ref).right_ref,
            color=self._follow(node.right_ref).color,
        )

    def rotate_right(self, node):
        return RedBlackNode(
            left_ref=self._follow(node.left_ref).left_ref,
            key=self._follow(node.left_ref).key, 
            value_ref=self._follow(node.left_ref).value_ref,
            right_ref=RedBlackNodeRef(
                referent=RedBlackNode.from_node(
                    node,
                    left_ref=self._follow(node.left_ref).right_ref
                )
            ),
            color=self._follow(node.left_ref).color,
        )

    def recolor(self, node):
        return RedBlackNode.from_node(
            node,
            left_ref=RedBlackNodeRef(referent=self._follow(node.left_ref).blacken()),
            right_ref=RedBlackNodeRef(referent=self._follow(node.right_ref).blacken()),
            color=Color.RED
        )

    def balance(self, node):
        if node.is_red():
            return node

        left = self._follow(node.left_ref)
        right = self._follow(node.right_ref)
        if left:
            left_left = self._follow(left.left_ref)
            left_right = self._follow(left.right_ref)
        else:
            left_left = None
            left_right = None

        if right:
            right_right = self._follow(right.right_ref)
            right_left = self._follow(right.left_ref)
        else:
            right_right = None
            right_left = None

        if left is not None and left.is_red():
            if right is not None and right.is_red():
                return self.recolor(node)
            if left_left is not None and left_left.is_red():
                return self.recolor(self.rotate_right(node))
            if left_right is not None and left_right.is_red():
                return self.recolor(self.rotate_right(
                    RedBlackNode.from_node(
                        node, 
                        left_ref=RedBlackNodeRef(
                            referent=self.rotate_left(left))
                    )))
            return node

        if right is not None and right.is_red():
            if right_right is not None and right_right.is_red():
                return self.recolor(self.rotate_left(node))
            if right_left is not None and right_left.is_red():
                return self.recolor(self.rotate_left(
                    RedBlackNode.from_node(
                        node,
                        right_ref=RedBlackNodeRef(
                            refernet=self.rotate_right(right))
                    )))
        return node

    def _follow(self, ref):
        """Get a node from a reference
        """
        #calls RedBlackNodeRef.get
        return ref.get(self._storage)


    # def update(self, node):
    #     if node.is_empty():
    #         return self
    #     if node.value < self.value:
    #         return RedBlackTree(
    #             self.left.update(node).balance(),
    #             self.value,
    #             self.right,
    #             color=self.color,
    #         ).balance()
    #     return RedBlackTree(
    #         self.left,
    #         self.value,
    #         self.right.update(node).balance(),
    #         color=self.color,
    #     ).balance()

    # def insert(self, value):
    #     return self.update(
    #         RedBlackTree(
    #             EmptyRedBlackTree(),
    #             value,
    #             EmptyRedBlackTree(),
    #             color=Color.RED,
    #         )
    #     ).blacken()

    # def is_member(self, value):
    #     if value < self._value:
    #         return self.left.is_member(value)
    #     if value > self._value:
    #         return self.right.is_member(value)
    #     return True



# class EmptyRedBlackTree(RedBlackTree):

#     def __init__(self):
#         self._color = Color.BLACK

#     def is_empty(self):
#         return True

#     def insert(self, value):
#         return RedBlackTree(
#             EmptyRedBlackTree(),
#             value,
#             EmptyRedBlackTree(),
#             color=Color.RED,
#         )

#     def update(self, node):
#         return node

#     def is_member(self, value):
#         return False

#     @property
#     def left(self):
#         return EmptyRedBlackTree()

#     @property
#     def right(self):
#         return EmptyRedBlackTree()

#     def __len__(self):
#         return 0