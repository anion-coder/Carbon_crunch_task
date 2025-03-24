import ast
import re
from typing import Dict, List
import radon.complexity as radon
from radon.metrics import mi_visit
import flake8.api.legacy as flake8

class PythonAnalyzer:
    def __init__(self):
        self.recommendations = []
        self.scores = {
            "naming": 0,
            "modularity": 0,
            "comments": 0,
            "formatting": 0,
            "reusability": 0,
            "best_practices": 0
        }

    def analyze(self, code: str) -> Dict:
        """
        Analyze Python code and return quality metrics and recommendations.
        """
        try:
            tree = ast.parse(code)
            self._analyze_naming(tree)
            self._analyze_modularity(code)
            self._analyze_comments(code)
            self._analyze_formatting(code)
            self._analyze_reusability(tree)
            self._analyze_best_practices(code)

            # Calculate overall score
            overall_score = sum(self.scores.values())

            return {
                "overall_score": overall_score,
                "breakdown": self.scores,
                "recommendations": self.recommendations
            }
        except SyntaxError as e:
            raise ValueError(f"Invalid Python code: {str(e)}")

    def _analyze_naming(self, tree: ast.AST):
        """Analyze naming conventions."""
        score = 10
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                    self.recommendations.append(
                        f"Function '{node.name}' should use snake_case naming convention."
                    )
                    score -= 2
            elif isinstance(node, ast.ClassDef):
                if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                    self.recommendations.append(
                        f"Class '{node.name}' should use PascalCase naming convention."
                    )
                    score -= 2
        self.scores["naming"] = max(0, score)

    def _analyze_modularity(self, code: str):
        """Analyze function length and complexity."""
        score = 20
        # Calculate cyclomatic complexity
        complexity = radon.cc_visit(code)
        for item in complexity:
            if item.complexity > 10:
                self.recommendations.append(
                    f"Function '{item.name}' is too complex (complexity: {item.complexity}). "
                    "Consider breaking it down into smaller functions."
                )
                score -= 5
        self.scores["modularity"] = max(0, score)

    def _analyze_comments(self, code: str):
        """Analyze comments and documentation."""
        score = 20
        lines = code.split('\n')
        docstring_count = 0
        comment_count = 0

        for line in lines:
            if line.strip().startswith('"""') or line.strip().startswith("'''"):
                docstring_count += 1
            elif line.strip().startswith('#'):
                comment_count += 1

        if docstring_count < 2:  # At least one docstring for module and main function
            self.recommendations.append("Add module and function docstrings.")
            score -= 5
        if comment_count < len(lines) * 0.1:  # At least 10% of lines should have comments
            self.recommendations.append("Add more inline comments to explain complex logic.")
            score -= 5
        self.scores["comments"] = max(0, score)

    def _analyze_formatting(self, code: str):
        """Analyze code formatting and indentation."""
        score = 15
        style_guide = flake8.get_style_guide()
        report = style_guide.check_files([code])
        if report.total_errors > 0:
            self.recommendations.append(
                f"Fix {report.total_errors} PEP 8 style violations."
            )
            score -= report.total_errors
        self.scores["formatting"] = max(0, score)

    def _analyze_reusability(self, tree: ast.AST):
        """Analyze code reusability and DRY principles."""
        score = 15
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        if len(functions) < 2:
            self.recommendations.append(
                "Consider breaking down the code into more reusable functions."
            )
            score -= 5
        self.scores["reusability"] = max(0, score)

    def _analyze_best_practices(self, code: str):
        """Analyze general best practices."""
        score = 20
        # Check for common anti-patterns
        anti_patterns = [
            (r'except:', "Use specific exception handling instead of bare 'except'."),
            (r'global\s+', "Avoid using global variables."),
            (r'print\s*\(', "Use logging instead of print statements in production code."),
        ]
        
        for pattern, message in anti_patterns:
            if re.search(pattern, code):
                self.recommendations.append(message)
                score -= 5
        self.scores["best_practices"] = max(0, score) 