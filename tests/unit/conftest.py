#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

"""Unit test fixtures - Only isolated, fast fixtures"""

import pytest

# Note: Unit tests should NOT use:
# - client fixture (use in integration tests)
# - sqlite_schema fixture (use in integration tests)
# - database connections (mock instead)
#
# Unit test fixtures should:
# - Be fast (microseconds to milliseconds)
# - Have no side effects
# - Test one thing in isolation
# - Mock external dependencies
