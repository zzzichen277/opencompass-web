"""OpenCompass integration service for evaluation execution."""

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.core.config import settings


class OpenCompassService:
    """Service for interacting with OpenCompass evaluation framework."""

    def __init__(self):
        """Initialize OpenCompass service."""
        self.data_dir = Path(settings.OPENCOMPASS_DATA_DIR)
        self.config_dir = self._get_opencompass_config_dir()

    def _get_opencompass_config_dir(self) -> Path:
        """Get OpenCompass configuration directory."""
        possible_paths = [
            Path(__file__).parent.parent.parent.parent / "opencompass" / "configs",
        ]
        for path in possible_paths:
            if path.exists():
                return path
        return self.data_dir / "configs"

    def get_builtin_datasets(self) -> List[Dict[str, Any]]:
        """Get list of built-in datasets from OpenCompass configs."""
        datasets = []
        datasets_dir = self.config_dir / "datasets"
        if not datasets_dir.exists():
            return self._get_default_datasets()

        for dataset_dir in datasets_dir.iterdir():
            if dataset_dir.is_dir() and not dataset_dir.name.startswith("_"):
                dataset_info = self._parse_dataset_config(dataset_dir)
                if dataset_info:
                    datasets.append(dataset_info)

        return datasets if datasets else self._get_default_datasets()

    def _parse_dataset_config(self, config_dir: Path) -> Optional[Dict[str, Any]]:
        """Parse dataset configuration from directory."""
        gen_configs = list(config_dir.glob("*_gen.py"))
        main_config = gen_configs[0] if gen_configs else None
        if not main_config:
            return None
        dataset_name = config_dir.name
        category = self._determine_category(dataset_name)
        return {
            "id": f"builtin_{dataset_name}",
            "name": dataset_name,
            "type": "builtin",
            "category": category,
            "description": f"OpenCompass built-in dataset: {dataset_name}",
            "config_path": str(main_config.relative_to(self.config_dir)),
            "metrics": ["accuracy"],
            "tags": [category],
        }

    def _determine_category(self, dataset_name: str) -> str:
        """Determine dataset category based on name."""
        name_lower = dataset_name.lower()
        if any(kw in name_lower for kw in ["math", "gsm8k", "aime"]):
            return "math"
        if any(kw in name_lower for kw in ["humaneval", "mbpp", "code"]):
            return "code"
        if any(kw in name_lower for kw in ["bbh", "bbeh", "musr", "arc"]):
            return "reasoning"
        return "qa"

    def _get_default_datasets(self) -> List[Dict[str, Any]]:
        """Get default dataset list."""
        return [
            {"id": "builtin_mmlu", "name": "MMLU", "type": "builtin", "category": "qa",
             "description": "Massive Multitask Language Understanding", "config_path": "datasets/mmlu/mmlu_gen.py",
             "metrics": ["accuracy"], "sample_count": 14042},
            {"id": "builtin_gsm8k", "name": "GSM8K", "type": "builtin", "category": "math",
             "description": "Grade School Math 8K", "config_path": "datasets/gsm8k/gsm8k_gen.py",
             "metrics": ["accuracy"], "sample_count": 1319},
            {"id": "builtin_humaneval", "name": "HumanEval", "type": "builtin", "category": "code",
             "description": "HumanEval Code Benchmark", "config_path": "datasets/humaneval/humaneval_gen.py",
             "metrics": ["pass@1"], "sample_count": 164},
        ]

    def generate_eval_config(
        self,
        task_name: str,
        models: List[Dict[str, Any]],
        datasets: List[str],
        accelerator: str = "huggingface",
    ) -> str:
        """Generate OpenCompass evaluation configuration file."""
        config_path = self.data_dir / "configs" / f"{task_name}.py"
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "w", encoding="utf-8") as f:
            f.write(f"# Auto-generated config for task: {task_name}\n\n")
            f.write(f"models = [\n")
            for model in models:
                f.write(f"    {{'type': 'HuggingFace', 'path': '{model.get('path', '')}'}}\n")
            f.write(f"]\n\n")
            f.write(f"datasets = {datasets}\n")

        return str(config_path)

    async def run_evaluation(
        self,
        config_path: str,
        task_id: str,
        progress_callback: Optional[callable] = None,
        log_callback: Optional[callable] = None,
    ) -> Dict[str, Any]:
        """Run OpenCompass evaluation."""
        cmd = [sys.executable, "-m", "opencompass", config_path]
        results = {"status": "completed", "scores": {}, "errors": []}

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                line_str = line.decode("utf-8", errors="ignore").strip()
                if line_str and log_callback:
                    await log_callback(task_id, "info", line_str)

            await process.wait()

            if process.returncode != 0:
                stderr = await process.stderr.read()
                results["status"] = "failed"
                results["errors"].append(stderr.decode("utf-8", errors="ignore"))

        except Exception as e:
            results["status"] = "failed"
            results["errors"].append(str(e))

        return results


opencompass_service = OpenCompassService()