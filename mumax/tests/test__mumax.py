# SPDX-FileCopyrightText: Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo@lunarbase.ai>
#
# SPDX-License-Identifier: GPL-3.0-or-later
from unittest.mock import patch, mock_open

import pytest

from mumax.src.mumax import Mumax


class TestMumax:

    def setup_method(self):
        self.component = Mumax()
        self.mock_url = "http://20.29.51.115:8000"

    @patch("builtins.open", new_callable=mock_open, read_data="mock data")
    @patch("requests.post")
    @patch("requests.get")
    def test_run_success(self, mock_get, mock_post, mock_file):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"error": "", "images": ["image1.png", "image2.png"]}
        result = self.component.run("mock_file.mx3")
        mock_post.assert_called_once_with(
            self.mock_url + "/upload/",
            headers={'accept': 'application/json'},
            files={"file": mock_file()}
        )
        mock_get.assert_called_once_with(self.mock_url + "/run-command/", params={"file_name": "mock_file.mx3"})
        assert result == {"result": "Success", "images": ["image1.png", "image2.png"]}

    @patch("builtins.open", new_callable=mock_open, read_data="mock data")
    @patch("requests.post")
    @patch("requests.get")
    def test_run_failure_response(self, mock_get, *_):
        mock_get.return_value.status_code = 500
        with pytest.raises(Exception, match="There has been an error 500"):
            self.component.run("mock_file.mx3")

    @patch("builtins.open", new_callable=mock_open, read_data="mock data")
    @patch("requests.post")
    @patch("requests.get")
    def test_run_main_go_error(self, mock_get, *_):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"error": "Error in main.go", "images": []}
        result = self.component.run("mock_file.mx3")
        assert result == {"result": "Error in main.go", "images": []}
