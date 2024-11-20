from typing import Any, Optional

from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType



class NewComponent(
  BaseComponent,
  component_name="New Component",
  component_description="""desc""",
  input_types={"text_input": DataType.TEXT},
  output_type=DataType.TEXT,
  component_group=ComponentGroup.CUSTOM,
  conf="cats too",
  
):
  def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
    super().__init__(model=model, configuration=kwargs)

  def run(self, text_input):
    return text_input + self.conf

