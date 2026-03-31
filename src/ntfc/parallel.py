############################################################################
# SPDX-License-Identifier: Apache-2.0
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.  The
# ASF licenses this file to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the
# License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations
# under the License.
#
############################################################################

"""Parallel execution utilities for handlers."""

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, List, TypeVar

T = TypeVar("T")


def run_parallel(
    items: List[T],
    fn: Callable[[T], Any],
) -> List[Any]:
    """Run a callable on all items in parallel, preserving order.

    :param items: List of objects to execute on.
    :param fn: Callable invoked with each item as its sole argument.
    :return: List of results in the same order as *items*.
    """
    if not items:
        return []

    with ThreadPoolExecutor(max_workers=len(items)) as executor:
        futures = [executor.submit(fn, item) for item in items]
        return [future.result() for future in futures]
