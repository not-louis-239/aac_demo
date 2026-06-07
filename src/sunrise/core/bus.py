# bus.py

# repo at: https://github.com/not-louis-239/sunrise-aac
# Copyright (C) 2026 Louis Masarei-Boulton <243234869+not-louis-239@users.noreply.github.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import weakref
from typing import Callable, Any
from enum import StrEnum


class EventID(StrEnum):
    STATE_CHANGE = "STATE_CHANGE"


class Bus:
    def __init__(self):
        # _listeners is {event_name, references_to_functions_to_call}
        self._listeners: dict[EventID, list[weakref.ref[Callable[..., Any]]]] = {}

    def subscribe(self, event_name: EventID, func: Callable) -> None:
        if event_name not in self._listeners:
            self._listeners[event_name] = []

        # If the function is a method of an object, we need to use weakref to avoid
        # memory leaks caused by the Bus holding on to strong references.
        if hasattr(func, "__self__"):
            ref = weakref.WeakMethod(func)
        else:
            ref = weakref.ref(func)

        self._listeners[event_name].append(ref)

    def emit(self, event_name: EventID, *args, **kwargs) -> None:
        if event_name not in self._listeners:
            return

        dead_listeners = []

        for ref in self._listeners[event_name][:]:
            try:
                func = ref()

                if func is None:
                    dead_listeners.append(ref)
                    continue

                func(*args, **kwargs)
            except ReferenceError:
                # Weak reference was garbage collected
                dead_listeners.append(ref)

        for dead in dead_listeners:
            if dead in self._listeners[event_name]:
                self._listeners[event_name].remove(dead)
