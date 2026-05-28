"""
Sandbox Executor - Safely executes generated code
"""

import subprocess
import os
import tempfile
import shutil
from typing import Dict, Any, Optional
from pathlib import Path

class SandboxExecutor:
    def __init__(self, sandbox_path: str = "./sandbox"):
        self.sandbox_path = sandbox_path
        os.makedirs(sandbox_path, exist_ok=True)

    def execute_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Execute code in a sandboxed environment"""
        
        # Validate code safety
        if not self._validate_code(code):
            return {
                "success": False,
                "error": "Code validation failed",
                "stdout": "",
                "stderr": "Potentially dangerous code blocked"
            }
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix=f'.{language}',
            delete=False,
            dir=self.sandbox_path
        ) as f:
            f.write(code)
            temp_path = f.name
        
        try:
            # Execute in sandbox
            if language == "python":
                result = subprocess.run(
                    ["python3", temp_path],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=self.sandbox_path
                )
            elif language == "javascript":
                result = subprocess.run(
                    ["node", temp_path],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=self.sandbox_path
                )
            else:
                return {
                    "success": False,
                    "error": f"Unsupported language: {language}"
                }
            
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Execution timeout (30s limit)"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def _validate_code(self, code: str) -> bool:
        """Basic code safety validation"""
        dangerous_patterns = [
            "import os; os.system",
            "subprocess.call(['rm",
            "subprocess.run(['rm",
            "__import__('os')",
            "__import__('subprocess')",
            "eval(input",
            "exec(input",
        ]
        
        for pattern in dangerous_patterns:
            if pattern in code:
                return False
        
        return True

    def cleanup(self):
        """Clean up sandbox directory"""
        if os.path.exists(self.sandbox_path):
            for item in os.listdir(self.sandbox_path):
                path = os.path.join(self.sandbox_path, item)
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)

    def test_file(self, file_path: str) -> Dict[str, Any]:
        """Test an existing file in the sandbox"""
        if not os.path.exists(file_path):
            return {"success": False, "error": "File not found"}
        
        with open(file_path, 'r') as f:
            code = f.read()
        
        extension = Path(file_path).suffix.lstrip('.')
        return self.execute_code(code, extension)