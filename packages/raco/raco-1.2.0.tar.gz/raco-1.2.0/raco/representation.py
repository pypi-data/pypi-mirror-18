

class RepresentationProperties(object):

    def __init__(
            self,
            hash_partitioned=frozenset(),
            sorted=None,
            grouped=None):
        """
        @param hash_partitioned: None or set of AttributeRefs in hash key
        @param sorted: None or list of (AttributeRefs, ASC/DESC) in sort order
        @param grouped: None or list of AttributeRefs to group by

        None means that no knowledge about the interesting property is
        known
        """

        # TODO: make it a set of sets, representing a conjunction of hashes
        # TODO: for example, after a HashJoin($1=$4) we know h($1) && h($4)
        # TODO:     which is not equivalent to h($1, $4). Currently can only
        # TODO:     represent conjunctions of size 1
        self.hash_partitioned = hash_partitioned

        if sorted is not None or grouped is not None:
            raise NotImplementedError("sorted and grouped not yet supported")

    def __str__(self):
        return "{clazz}(hash: {hash_attrs})".format(
            clazz=self.__class__.__name__,
            hash_attrs=self.hash_partitioned)

    def __repr__(self):
        return "{clazz}({hp!r}, {sort!r}, {grp!r})".format(
            clazz=self.__class__.__name__,
            hp=self.hash_partitioned,
            sort=None,
            grp=None
        )
