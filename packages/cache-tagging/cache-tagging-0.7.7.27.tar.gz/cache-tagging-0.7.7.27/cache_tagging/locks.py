import time
import operator
import threading
import collections
from functools import reduce
from cache_tagging.exceptions import TagLocked
from cache_tagging.interfaces import ITagsLock
from cache_tagging.utils import get_thread_id, make_tag_key, to_hashable


TagBean = collections.namedtuple('TagBean', ('time', 'status', 'thread_id'))


class TagsLock(ITagsLock):

    def __init__(self, thread_safe_cache_accessor, delay=None):
        self._cache = thread_safe_cache_accessor
        self._delay = delay  # For master/slave

    def get_tag_versions(self, tags, transaction_start_time, version=None):
        return self._get_tag_versions(tags, version).pop()

    def _get_tag_versions(self, tags, version=None):
        tag_keys = {tag: make_tag_key(tag) for tag in tags}
        deferred = GetManyDeferred(self._cache().get_many, version)
        deferred.append(
            lambda _, caches: {tag: caches[tag_key] for tag, tag_key in tag_keys.items() if tag_key in caches},
            tag_keys.values()
        )
        return deferred

    @staticmethod
    def make(isolation_level, thread_safe_cache_accessor, delay):
        if isolation_level == 'READ UNCOMMITED':
            return ReadUncommittedTagsLock(thread_safe_cache_accessor, delay)
        elif isolation_level == 'READ COMMITED':
            return ReadCommittedTagsLock(thread_safe_cache_accessor, delay)
        elif isolation_level == 'REPEATABLE READS':
            return RepeatableReadsTagsLock(thread_safe_cache_accessor, delay)
        elif isolation_level == 'SERIALIZABLE':
            return SerializableTagsLock(thread_safe_cache_accessor, delay)


class ReadUncommittedTagsLock(TagsLock):
    """
    Tag Lock for Read Ucnommited and higher transaction isolation level.
    """
    def acquire_tags(self, tags, version=None):
        pass

    def release_tags(self, tags, version=None):
        if self._delay:
            threading.Timer(self._delay, self._release_tags_delayed, [tags, version]).start()

    def _release_tags_delayed(self, tags, version=None):
        self._cache().delete_many(list(map(make_tag_key, tags)), version=version)


class ReadCommittedTagsLock(ReadUncommittedTagsLock):
    def release_tags(self, tags, version=None):
        self._release_tags_delayed(tags, version)
        super(ReadCommittedTagsLock, self).release_tags(tags, version)


class RepeatableReadsTagsLock(TagsLock):
    """
    Tag Lock for Repeatable Reads and higher transaction isolation level.
    """
    LOCK_PREFIX = "lock"
    LOCK_TIMEOUT = 5

    class STATUS(object):
        ASQUIRED = 0
        RELEASED = 1

    def acquire_tags(self, tags, version=None):
        return self._set_tags_status(tags, self.STATUS.ASQUIRED, version)

    def release_tags(self, tags, version=None):
        return self._set_tags_status(tags, self.STATUS.RELEASED, version)

    def _set_tags_status(self, tags, status, version=None):
        """Locks tags for concurrent transactions."""
        data = TagBean(time.time(), status, get_thread_id())
        self._cache().set_many(
            {self._make_locked_tag_key(tag): data for tag in tags}, self._get_timeout(), version
        )

    def _make_locked_tag_key(self, tag):
        return '{0}_{1}'.format(self.LOCK_PREFIX, make_tag_key(tag))

    def _get_timeout(self):
        timeout = self.LOCK_TIMEOUT
        if self._delay:
            timeout += self._delay
        return timeout

    def get_tag_versions(self, tags, transaction_start_time, version=None):
        """Returns tags dict if all tags is not locked.

        Raises TagLocked, if current transaction has been started earlier
        than any tag has been invalidated by concurent process.
        Actual for SERIALIZABLE and REPEATABLE READ transaction levels.
        """
        deferred = self._get_tag_versions(tags, version)
        deferred += self._get_locked_tags(tags, transaction_start_time, version)
        locked_tags = deferred.pop()
        if locked_tags:
            raise TagLocked(locked_tags)
        return deferred.pop()

    def _get_locked_tags(self, tags, transaction_start_time, version=None):
        tag_keys = {tag: self._make_locked_tag_key(tag) for tag in tags}

        def callback(_, caches):
            locked_tag_caches = {tag: caches[tag_key] for tag, tag_key in tag_keys.items() if tag_key in caches}
            return set(tag for tag, tag_bean in locked_tag_caches.items()
                       if self._tag_is_locked(tag_bean, transaction_start_time))

        deferred = GetManyDeferred(self._cache().get_many, version)
        deferred.append(callback, tag_keys.values())
        return deferred

    def _tag_is_locked(self, tag_bean, transaction_start_time):
        if tag_bean.thread_id == get_thread_id():
            # Acquired by current thread, ignore it
            return False
        if tag_bean.status == self.STATUS.ASQUIRED:
            # Tag still is asquired
            return True
        if transaction_start_time <= (tag_bean.time + self._delay):
            # We don't create cache in all transactions started earlier than finished the transaction which has invalidated tag.
            return True


class SerializableTagsLock(RepeatableReadsTagsLock):
    pass


class AbstractDeferred(object):

    def __init__(self, executor, *args, **kwargs):
        self.execute = executor
        self.args = args
        self.kwargs = kwargs
        self.queue = []
        self.parent = None
        self._iterator = None
        self.key = to_hashable((self.execute, self.args, self.kwargs))

    def append(self, callback, *args, **kwargs):
        self.queue.append([callback, args, kwargs])
        return self

    def pop(self):
        if self._iterator is None:
            self._iterator = iter(self)
        return next(self._iterator)

    def __add__(self, other):
        result = self.__class__(self.execute, *self.args, **self.kwargs)
        result += self
        result += other
        return result

    def __iadd__(self, other):
        """
        :type other: cache_tagging.locks.Deferred
        :rtype: cache_tagging.locks.Deferred
        """
        if self.key == other.key:
            self.queue.extend(other.queue)
            return self
        else:
            other.parent = self
            return other

    def __iter__(self):
        raise NotImplementedError


class GetManyDeferred(AbstractDeferred):
    def __iter__(self):
        return iter(GetManyDeferredIterator(self))


class GetManyDeferredIterator(object):
    def __init__(self, deferred):
        """
        :type deferred: cache_tagging.locks.Deferred
        """
        self._deferred = deferred

    def __iter__(self):
        visited_node_keys = {}
        node = self._deferred
        while node:
            if node.key not in visited_node_keys:
                visited_node_keys[node.key] = node.execute(list(self.get_keys(node.key)), *node.args, **node.kwargs) or {}
            result = visited_node_keys[node.key]
            for i in self._iter_node(node, result):
                yield i
            node = node.parent

    @staticmethod
    def _iter_node(node, result):
        for i in reversed(node.queue):
            yield i[0](node, {key: result[key] for key in i[1][0] if key in result})

    def get_keys(self, node_key):
        keys = set()
        node = self._deferred
        while node:
            if node.key == node_key:
                keys |= self.get_node_keys(node)
            node = node.parent
        return keys

    @staticmethod
    def get_node_keys(node):
        return reduce(operator.or_, map(set, map(operator.itemgetter(0), map(operator.itemgetter(1), node.queue))))
