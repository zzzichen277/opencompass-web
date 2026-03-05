"""Report generation service for evaluation results."""

import io
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape


class ReportService:
    """Service for generating evaluation reports."""

    def __init__(self):
        """Initialize report service."""
        self.env = Environment(
            loader=FileSystemLoader(searchpath="./templates"),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def generate_html_report(
        self,
        task_name: str,
        task_description: Optional[str],
        results: Dict[str, Any],
        models: List[Dict[str, Any]],
        datasets: List[Dict[str, Any]],
    ) -> str:
        """Generate HTML report for evaluation results.

        Args:
            task_name: Name of the evaluation task
            task_description: Optional task description
            results: Evaluation results dictionary
            models: List of evaluated models
            datasets: List of evaluation datasets

        Returns:
            HTML string of the report
        """
        # Build HTML report
        html = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>评测报告 - {task_name}</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    line-height: 1.6;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    color: #333;
                }}
                h1, h2, h3 {{
                    color: #2c3e50;
                }}
                .header {{
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }}
                .summary {{
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }}
                th {{
                    background: #3498db;
                    color: white;
                }}
                tr:nth-child(even) {{
                    background: #f2f2f2;
                }}
                .score-high {{ color: #27ae60; font-weight: bold; }}
                .score-mid {{ color: #f39c12; font-weight: bold; }}
                .score-low {{ color: #e74c3c; font-weight: bold; }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 10px;
                    border-top: 1px solid #ddd;
                    color: #666;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>评测报告</h1>
                <p><strong>任务名称:</strong> {task_name}</p>
                {f'<p><strong>任务描述:</strong> {task_description}</p>' if task_description else ''}
                <p><strong>生成时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>

            <div class="summary">
                <h2>评测概览</h2>
                <p><strong>评测模型数量:</strong> {len(models)}</p>
                <p><strong>评测数据集数量:</strong> {len(datasets)}</p>
            </div>

            <h2>评测模型</h2>
            <table>
                <tr>
                    <th>模型名称</th>
                    <th>类型</th>
                    <th>路径/配置</th>
                </tr>
                {''.join(f'<tr><td>{m.get("name", "N/A")}</td><td>{m.get("type", "N/A")}</td><td>{m.get("path", m.get("api_config", {}).get("base_url", "N/A"))}</td></tr>' for m in models)}
            </table>

            <h2>评测数据集</h2>
            <table>
                <tr>
                    <th>数据集名称</th>
                    <th>类别</th>
                    <th>样本数量</th>
                </tr>
                {''.join(f'<tr><td>{d.get("name", "N/A")}</td><td>{d.get("category", "N/A")}</td><td>{d.get("sample_count", "N/A")}</td></tr>' for d in datasets)}
            </table>

            <h2>评测结果</h2>
            {self._generate_results_table(results)}

            <div class="footer">
                <p>此报告由 OpenCompass Web Platform 自动生成</p>
            </div>
        </body>
        </html>
        """

        return html

    def _generate_results_table(self, results: Dict[str, Any]) -> str:
        """Generate results table HTML."""
        scores = results.get("scores", {})
        if not scores:
            return "<p>暂无评测结果</p>"

        rows = []
        for key, value in scores.items():
            if isinstance(value, (int, float)):
                score_class = "score-high" if value >= 80 else ("score-mid" if value >= 60 else "score-low")
                rows.append(f"<tr><td>{key}</td><td class='{score_class}'>{value:.2f}%</td></tr>")
            elif isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, (int, float)):
                        score_class = "score-high" if sub_value >= 80 else ("score-mid" if sub_value >= 60 else "score-low")
                        rows.append(f"<tr><td>{key} / {sub_key}</td><td class='{score_class}'>{sub_value:.2f}%</td></tr>")

        return f"""
        <table>
            <tr>
                <th>指标</th>
                <th>得分</th>
            </tr>
            {''.join(rows)}
        </table>
        """

    def generate_excel_data(
        self,
        task_name: str,
        results: Dict[str, Any],
        models: List[Dict[str, Any]],
        datasets: List[Dict[str, Any]],
    ) -> bytes:
        """Generate Excel file data for evaluation results.

        Args:
            task_name: Name of the evaluation task
            results: Evaluation results dictionary
            models: List of evaluated models
            datasets: List of evaluation datasets

        Returns:
            Excel file bytes
        """
        try:
            import pandas as pd
            from io import BytesIO

            # Create DataFrames
            model_df = pd.DataFrame(models)
            dataset_df = pd.DataFrame(datasets)

            # Create scores DataFrame
            scores = results.get("scores", {})
            scores_data = []
            for key, value in scores.items():
                if isinstance(value, (int, float)):
                    scores_data.append({"指标": key, "得分": value})
                elif isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        if isinstance(sub_value, (int, float)):
                            scores_data.append({"指标": f"{key}/{sub_key}", "得分": sub_value})

            scores_df = pd.DataFrame(scores_data)

            # Write to Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                model_df.to_excel(writer, sheet_name='模型', index=False)
                dataset_df.to_excel(writer, sheet_name='数据集', index=False)
                scores_df.to_excel(writer, sheet_name='评测结果', index=False)

            return output.getvalue()

        except ImportError:
            # Return CSV fallback if pandas not available
            return self._generate_csv_data(task_name, results, models, datasets)

    def _generate_csv_data(
        self,
        task_name: str,
        results: Dict[str, Any],
        models: List[Dict[str, Any]],
        datasets: List[Dict[str, Any]],
    ) -> bytes:
        """Generate CSV data as fallback."""
        import csv
        from io import StringIO

        output = StringIO()
        writer = csv.writer(output)

        writer.writerow([f"评测报告: {task_name}"])
        writer.writerow([f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
        writer.writerow([])

        # Models
        writer.writerow(["评测模型"])
        writer.writerow(["名称", "类型", "路径"])
        for m in models:
            writer.writerow([m.get("name", ""), m.get("type", ""), m.get("path", "")])
        writer.writerow([])

        # Datasets
        writer.writerow(["评测数据集"])
        writer.writerow(["名称", "类别", "样本数"])
        for d in datasets:
            writer.writerow([d.get("name", ""), d.get("category", ""), d.get("sample_count", "")])
        writer.writerow([])

        # Results
        writer.writerow(["评测结果"])
        writer.writerow(["指标", "得分"])
        scores = results.get("scores", {})
        for key, value in scores.items():
            if isinstance(value, (int, float)):
                writer.writerow([key, f"{value:.2f}%"])

        return output.getvalue().encode('utf-8')


# Singleton instance
report_service = ReportService()