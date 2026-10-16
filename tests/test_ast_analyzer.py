from modules.ast_analyzer import ASTAnalyzer


def test_analyze_collects_structure_and_counts_each_scope_once():
    source = """\
import os
from pathlib import Path

if os.name:
    enabled = True

def greet(name):
    if name:
        return name
    return "guest"

class Worker:
    def run(self, items):
        for item in items:
            print(item)
"""

    result = ASTAnalyzer().analyze(source)

    assert result.imports == ["os", "pathlib.Path"]
    assert [function.name for function in result.functions] == ["greet"]
    assert result.functions[0].complexity == 2
    assert [class_data.name for class_data in result.classes] == ["Worker"]
    assert result.classes[0].methods[0].complexity == 2
    # module 2 + greet 2 + Worker.run 2
    assert result.complexity_score == 6
    assert result.errors == []


def test_nested_function_complexity_is_not_added_to_parent_scope():
    source = """\
def outer():
    def inner(value):
        if value:
            return value
    return inner(1)
"""

    result = ASTAnalyzer().analyze(source)

    complexities = {function.name: function.complexity for function in result.functions}
    assert complexities == {"outer": 1, "inner": 2}
    # module 1 + outer 1 + inner 2
    assert result.complexity_score == 4


def test_syntax_error_is_reported_without_raising():
    result = ASTAnalyzer().analyze("def broken(:\n    pass")

    assert result.functions == []
    assert result.complexity_score == 0
    assert result.errors
    assert result.errors[0].startswith("SyntaxError 1번째 줄:")
