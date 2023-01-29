from dataclasses import dataclass
from typing import List, Dict
import os
from utils import get_project_root_path


@dataclass
class Design:
    # Define a design
    design_path: str
    source_files: List[str]
    test_files: List[str]
    executable_name: str


# Available designs
designs: Dict[str, Design] = {
    "simple_counter": Design(
        design_path=os.path.join(
            get_project_root_path(), "designs", "simple_counter"),
        source_files=[
            "simple_counter_top.v"
        ],
        test_files=[
            "simple_counter_test.cpp"
        ],
        executable_name="simple_counter_test"
    )
}
