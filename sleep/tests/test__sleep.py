# sleep/src/sleep/test___init__.py

# SPDX-FileCopyrightText: Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>
#
# SPDX-License-Identifier: GPL-3.0-or-later
from sleep import Sleep
from unittest.mock import patch
import time


class TestSleep:
    def setup_method(self):
        self.sleep_component = Sleep()

    def test_run_with_zero_timeout_no_mock(self):
        input_data = "test_data"
        timeout = 0
        start_time = time.time()
        result = self.sleep_component.run(input=input_data, timeout=timeout)
        end_time = time.time()
        assert result == input_data
        assert (end_time - start_time) < 0.1

    @patch('time.sleep', return_value=None)
    def test_time_timeout_can_be_called(self, mock_sleep):
        input_data = "test_data"
        timeout = 10
        result = self.sleep_component.run(input=input_data, timeout=timeout)
        mock_sleep.assert_called_once_with(timeout)
        assert result == input_data

    def test_run_with_two_timeout_no_mock(self):
        input_data = "test_data"
        timeout = 2
        start_time = time.time()
        result = self.sleep_component.run(input=input_data, timeout=timeout)
        end_time = time.time()
        assert result == input_data
        assert (end_time - start_time) >= 2