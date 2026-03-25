import ast
# Python 내장 모듈, 설치 불필요
# 코드 문자열을 트리 구조로 변환해줘요

import textwrap
# 들여쓰기 정규화 도구
# 코드 앞에 불필요한 공백이 있으면 ast.parse가 에러를 내요
# textwrap.dedent()로 제거해요
# 예: "    def foo():" → "def foo():"

from dataclasses import dataclass, field
# dataclass: 데이터 담는 클래스를 간단하게 만드는 문법
# __init__ 직접 안 써도 돼요
#
# field(default_factory=list):
# 리스트를 기본값으로 쓸 때 반드시 이렇게 써야 해요
# 그냥 [] 쓰면 모든 인스턴스가 같은 리스트 공유하는 버그 생겨요


# ── 내부 데이터 구조 ──────────────────────────────────────
# schemas.py는 FastAPI 응답용 (외부로 내보내는 형태)
# 여기 dataclass는 분석기 내부에서만 쓰는 형태
# 역할 분리 → 나중에 수정하기 편해요

@dataclass
class FunctionData:
    name: str
    lineno: int
    args: list[str]
    is_async: bool
    complexity: int

@dataclass
class ClassData:
    name: str
    lineno: int
    bases: list[str]
    methods: list[FunctionData]

@dataclass
class ASTResult:
    functions: list[FunctionData] = field(default_factory=list)
    classes: list[ClassData] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    total_lines: int = 0
    complexity_score: int = 0


# ── 분석기 본체 ───────────────────────────────────────────
# ast.NodeVisitor 상속받아요
# 이게 Visitor 패턴의 핵심
# → visit_XXX 정의하면 해당 노드 만날 때 자동 호출

class ASTAnalyzer(ast.NodeVisitor):

    def __init__(self):
        self.result = ASTResult()

        # 현재 방문 중인 클래스 추적용
        # 함수가 클래스 안인지 밖인지 구별할 때 사용
        self._current_class: ClassData | None = None

    def analyze(self, source_code: str) -> ASTResult:
        """외부에서 호출하는 메인 메서드"""

        # 분석할 때마다 결과 초기화
        self.result = ASTResult()
        self.result.total_lines = source_code.count("\n") + 1

        try:
            # 문자열 코드 → AST 트리 변환
            tree = ast.parse(textwrap.dedent(source_code))

            # 트리 순회 시작
            # 이 한 줄이 visit_XXX들을 전부 자동 호출해요
            self.visit(tree)

        except SyntaxError as e:
            # 문법 오류 → 서버 죽으면 안 되니까 에러 기록하고 반환
            self.result.errors.append(f"SyntaxError {e.lineno}번째 줄: {e.msg}")
            return self.result

        #일반 함수 복잡도 합산
        func_complexity = sum(f.complexity for f in self.result.functions)

        #클래스 메서드 복잡도 합산
        method_complexity = sum(
            m.complexity
            for c in self.result.classes
            for m in c.methods
        )
        self.result.complexity_score = func_complexity + method_complexity
        return self.result

    # ── Import 수집 ──────────────────────────────────────────

    def visit_Import(self, node: ast.Import) -> None:
        # "import os" / "import os, sys" 처리
        for alias in node.names:
            self.result.imports.append(alias.name)

        # generic_visit: 자식 노드 계속 순회
        # 빠뜨리면 이 노드 아래는 탐색 안 해요
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        # "from os import path" 처리
        # node.module = "os" / alias.name = "path"
        module = node.module or ""
        for alias in node.names:
            self.result.imports.append(f"{module}.{alias.name}")
        self.generic_visit(node)

    # ── 클래스 수집 ───────────────────────────────────────────

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        bases = [self._get_name(b) for b in node.bases]

        class_data = ClassData(
            name=node.name,
            lineno=node.lineno,
            bases=bases,
            methods=[],
        )

        # 클래스 내부 진입 전 현재 클래스 기록
        prev = self._current_class       # 중첩 클래스 대비 이전 값 저장
        self._current_class = class_data
        self.generic_visit(node)         # 내부 순회 (메서드들 탐색)
        self._current_class = prev       # 순회 끝나면 복원

        self.result.classes.append(class_data)

    # ── 함수/메서드 수집 ──────────────────────────────────────

    def _visit_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        args = [a.arg for a in node.args.args]

        func_data = FunctionData(
            name=node.name,
            lineno=node.lineno,
            args=args,
            is_async=isinstance(node, ast.AsyncFunctionDef),
            complexity=self._calc_complexity(node),
        )

        # _current_class 있으면 → 메서드
        # 없으면 → 일반 함수
        if self._current_class:
            self._current_class.methods.append(func_data)
        else:
            self.result.functions.append(func_data)

        self.generic_visit(node)

    # 동기/비동기 둘 다 같은 메서드로 처리
    visit_FunctionDef = _visit_function
    visit_AsyncFunctionDef = _visit_function

    # ── 유틸 메서드 ───────────────────────────────────────────

    @staticmethod
    def _get_name(node: ast.expr) -> str:
        """AST 노드에서 이름 문자열 추출"""
        if isinstance(node, ast.Name):
            return node.id                          # 단순 이름: "Bar"
        if isinstance(node, ast.Attribute):
            return f"{ASTAnalyzer._get_name(node.value)}.{node.attr}"  # "torch.nn"
        return ast.unparse(node)                    # 그 외 복잡한 표현식

    @staticmethod
    def _calc_complexity(node: ast.AST) -> int:
        """
        Cyclomatic Complexity (순환 복잡도)

        분기가 많을수록 코드가 복잡하고 버그가 숨기 쉬워요
        분기 노드 개수 + 1 로 계산해요

        분기 없는 함수  → 복잡도 1
        if 하나        → 복잡도 2
        if + for       → 복잡도 3
        """
        branch_nodes = (
            ast.If, ast.For, ast.While,
            ast.ExceptHandler, ast.With, ast.BoolOp,
        )
        # ast.walk: 노드 아래 모든 자식을 평탄하게 순회
        count = sum(1 for n in ast.walk(node) if isinstance(n, branch_nodes))
        return count + 1