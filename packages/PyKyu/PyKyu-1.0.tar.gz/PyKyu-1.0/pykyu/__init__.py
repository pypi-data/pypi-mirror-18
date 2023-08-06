# -*- coding: utf-8 -*-
import logging
from copy import deepcopy
from typing import List, Callable, Tuple

HookCallable = Callable[['KyuState'], None]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Kyu(object):
    def __init__(self, name):
        self.name = name
        logger.info(name)
        self.groups = list()
        self.groups_named = dict()

    def group(self, name):
        if name not in self.groups_named:
            group = KyuGroup(name)
            self.groups.append(group)
            self.groups_named[name] = group

        return self.groups_named[name]

    def flatten(self):
        for group in self.groups:
            for hook in group.hooks:
                yield group, hook

    def cursor(self, state: 'KyuState') -> 'KyuCursor':
        return KyuCursor(self, state)

    def run(self, state: 'KyuState') -> 'KyuState':
        cursor = self.cursor(state)
        # run them all
        for item in iter(cursor):
            logger.info(item.name)
            item.callback(cursor.state)

        return state


class KyuGroup(object):
    def __init__(self, name):
        self.name = name
        self.hooks = list()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def hook(self, callback: HookCallable, priority: int = 50):
        self.hooks.append(KyuHook(callback, priority, len(self.hooks)))
        self.hooks.sort(key=lambda x: (x.priority, x.index))
        return self


class KyuHook(object):
    def __init__(self, callback: HookCallable, priority: int, index: int):
        self.name = '%s.%s' % (callback.__module__, callback.__name__)
        self.callback = callback
        self.priority = priority
        self.index = index


class KyuCursor(object):
    def __init__(self, kyu, state: 'KyuState'):
        self._kyu = deepcopy(kyu)  # type: Kyu
        self._kyu_dirty = False
        self._kyu_flatten = None  # type: List[KyuHook]
        self._index = 0
        self.state = state
        self.state.cursor = self

    @property
    def kyu(self):
        self._kyu_dirty = True
        return self._kyu

    def flatten(self) -> List[Tuple['KyuGroup', 'KyuHook']]:
        if self._kyu_flatten is None or self._kyu_dirty:
            self._kyu_flatten = list(self._kyu.flatten())
        return self._kyu_flatten

    def _item_at(self, index) -> Tuple['KyuGroup', 'KyuHook']:
        flatten = self.flatten()
        if 0 <= index <= len(flatten) - 1:
            return flatten[index]
        else:
            return None, None

    def _group_at(self, index) -> 'KyuGroup':
        return self._item_at(index)[0]

    def _hook_at(self, index) -> 'KyuHook':
        return self._item_at(index)[1]

    @property
    def current(self):
        return self._hook_at(self._index)

    @property
    def peek_previous(self):
        return self._hook_at(self._index - 1)

    @property
    def peek_next(self):
        return self._hook_at(self._index + 1)

    def __iter__(self):
        self.reset()
        while True:
            yield self.current
            self.next()

    def reset(self):
        self._index = 0

    def next(self):
        if self._index + 1 > len(self.flatten()) - 1:
            raise StopIteration
        self._index += 1
        return self.current

    def skip_group(self):
        group = self._group_at(self._index)
        while True:
            self.next()
            if self._group_at(self._index + 1) is not group:
                break

    def skip_to_end(self):
        self._index = len(self.flatten()) - 1


class KyuState(object):
    def __init__(self):
        self.cursor = None  # type: KyuCursor
        self.data = dict()
