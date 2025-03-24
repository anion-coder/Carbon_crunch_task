import re
from typing import Dict, List
import esprima
from esprima import nodes

class JavaScriptAnalyzer:
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
        Analyze JavaScript code and return quality metrics and recommendations.
        """
        try:
            tree = esprima.parseScript(code, {'loc': True, 'range': True})
            self._analyze_naming(tree)
            self._analyze_modularity(tree)
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
        except esprima.Error as e:
            raise ValueError(f"Invalid JavaScript code: {str(e)}")

    def _analyze_naming(self, tree: nodes.Node):
        """Analyze naming conventions."""
        score = 10
        for node in esprima.NodeVisitor().visit(tree):
            if isinstance(node, nodes.FunctionDeclaration):
                if not re.match(r'^[a-z][a-zA-Z0-9]*$', node.id.name):
                    self.recommendations.append(
                        f"Function '{node.id.name}' should use camelCase naming convention."
                    )
                    score -= 2
            elif isinstance(node, nodes.VariableDeclarator):
                if not re.match(r'^[a-z][a-zA-Z0-9]*$', node.id.name):
                    self.recommendations.append(
                        f"Variable '{node.id.name}' should use camelCase naming convention."
                    )
                    score -= 2
        self.scores["naming"] = max(0, score)

    def _analyze_modularity(self, tree: nodes.Node):
        """Analyze function length and complexity."""
        score = 20
        for node in esprima.NodeVisitor().visit(tree):
            if isinstance(node, nodes.FunctionDeclaration):
                # Count function body statements
                if hasattr(node.body, 'body'):
                    statement_count = len(node.body.body)
                    if statement_count > 20:
                        self.recommendations.append(
                            f"Function '{node.id.name}' is too long ({statement_count} statements). "
                            "Consider breaking it down into smaller functions."
                        )
                        score -= 5
        self.scores["modularity"] = max(0, score)

    def _analyze_comments(self, code: str):
        """Analyze comments and documentation."""
        score = 20
        lines = code.split('\n')
        comment_count = 0
        jsdoc_count = 0

        for line in lines:
            if line.strip().startswith('//'):
                comment_count += 1
            elif line.strip().startswith('/*'):
                jsdoc_count += 1

        if jsdoc_count < 1:  # At least one JSDoc comment
            self.recommendations.append("Add JSDoc comments for functions and classes.")
            score -= 5
        if comment_count < len(lines) * 0.1:  # At least 10% of lines should have comments
            self.recommendations.append("Add more inline comments to explain complex logic.")
            score -= 5
        self.scores["comments"] = max(0, score)

    def _analyze_formatting(self, code: str):
        """Analyze code formatting and indentation."""
        score = 15
        # Check for common formatting issues
        formatting_issues = [
            (r'if\s*\(', "Add space after 'if' keyword."),
            (r'for\s*\(', "Add space after 'for' keyword."),
            (r'while\s*\(', "Add space after 'while' keyword."),
            (r'function\s*\(', "Add space after 'function' keyword."),
        ]
        
        for pattern, message in formatting_issues:
            if re.search(pattern, code):
                self.recommendations.append(message)
                score -= 2
        self.scores["formatting"] = max(0, score)

    def _analyze_reusability(self, tree: nodes.Node):
        """Analyze code reusability and DRY principles."""
        score = 15
        functions = [node for node in esprima.NodeVisitor().visit(tree) 
                    if isinstance(node, nodes.FunctionDeclaration)]
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
            (r'var\s+', "Use 'const' or 'let' instead of 'var'."),
            (r'console\.log', "Remove console.log statements from production code."),
            (r'eval\s*\(', "Avoid using eval() as it can lead to security issues."),
            (r'==\s*', "Use strict equality (===) instead of loose equality (==)."),
        ]
        
        for pattern, message in anti_patterns:
            if re.search(pattern, code):
                self.recommendations.append(message)
                score -= 5
        self.scores["best_practices"] = max(0, score) 