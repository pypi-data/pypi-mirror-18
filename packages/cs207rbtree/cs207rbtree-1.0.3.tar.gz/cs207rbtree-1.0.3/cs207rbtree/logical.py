class ValueRef(object):
    "A reference to a string value on disk"
    def __init__(self, referent=None, address=0):
        self._referent = referent #value to store
        self._address = address #address to store at
        
    @property
    def address(self):
        return self._address

    def prepare_to_store(self, storage):
        """Need to be overridden by subclass (BinaryNodeRef)
        """
        pass

    @staticmethod
    def referent_to_bytes(referent):
        return referent.encode('utf-8')

    @staticmethod
    def bytes_to_referent(bytes):
        return bytes.decode('utf-8')

    def get(self, storage):
        "Read bytes for value from disk"
        if self._referent is None and self._address:
            self._referent = self.bytes_to_referent(storage.read(self._address))
        return self._referent

    def store(self, storage):
        "Store bytes for value to disk"
        #called by BinaryNode.store_refs
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_bytes(self._referent))


            