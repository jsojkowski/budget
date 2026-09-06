from budget.budget_latex import LatexIO
from budget.budget_yaml import YamlIO
from budget.budget_io import IOType

class IOFactory:

    def __init__(self):
        self.io_map = {}

    def get_io(self, type: IOType) -> IOType:
        match type:
            case IOType.YAML:
                if IOType.YAML not in self.io_map.keys():
                    self.io_map[IOType.YAML] = YamlIO()
                return self.io_map[IOType.YAML]
            case IOType.LATEX:
                if IOType.LATEX not in self.io_map.keys():
                    self.io_map[IOType.LATEX] = LatexIO()
                return self.io_map[IOType.LATEX]
            # case IOType.XLXS:
            #     if IOType.XLXS not in self.io_map.keys():
            #         self.io_map[IOType.XLXS] = XlxsBudgetIO()
            #     return self.io_map[IOType.XLXS]
            case _:  # Default case for any other value
                print("Unknown menu option. Saving content and exiting.")
                return None
