"""
Tests for sandbox executor
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sandbox import SandboxExecutor

class TestSandboxExecutor:
    def setup_method(self):
        self.sandbox = SandboxExecutor("./test_sandbox")

    def test_execute_safe_python(self):
        result = self.sandbox.execute_code("print('Hello, World!')", "python")
        assert result["success"] == True
        assert "Hello" in result["stdout"]

    def test_execute_with_error(self):
        result = self.sandbox.execute_code("print(undefined_var)", "python")
        assert result["success"] == False

    def test_block_dangerous_code(self):
        result = self.sandbox.execute_code("import os; os.system('rm -rf')", "python")
        assert result["success"] == False

    def test_timeout(self):
        code = "import time; time.sleep(60)"
        result = self.sandbox.execute_code(code, "python")
        assert result["success"] == False
        assert "timeout" in result.get("error", "").lower()

    def teardown_method(self):
        self.sandbox.cleanup()
        if os.path.exists("./test_sandbox"):
            import shutil
            shutil.rmtree("./test_sandbox")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])