# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Lunarbase <contact@lunarbase.ai>
#
# SPDX-License-Identifier: LicenseRef-lunarbase

import os
import pytest
from url2html import URL2HTML

@pytest.mark.asyncio
async def test_url2html_conversion():
    component = URL2HTML()
    url = "https://example.com"
    
    result = await component.run(url)
    
    assert result is not None
    assert os.path.exists(result)
    assert result.endswith(".html")
    
    with open(result, "r", encoding="utf-8") as f:
        content = f.read()
        assert "<html" in content.lower()
        assert "</html>" in content.lower()

@pytest.mark.asyncio
async def test_url2html_invalid_url():
    component = URL2HTML()
    url = "https://this-is-an-invalid-url-that-does-not-exist.com"
    
    result = await component.run(url)
    
    assert result is None

@pytest.mark.asyncio
async def test_url2html_special_characters():
    component = URL2HTML()
    url = "https://example.com/path/with/special/chars!@#$%^&*()"
    
    result = await component.run(url)
    
    assert result is not None
    assert os.path.exists(result)
    assert "special_chars" in result
    assert result.endswith(".html") 