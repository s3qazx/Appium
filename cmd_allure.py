"""生成 Allure 3 HTML 报告：uv run python cmd_allure.py。"""
import subprocess
from pathlib import Path


def main():
    project_dir = Path(__file__).resolve().parent
    # Allure 3 不支持旧版的 --clean 参数。
    subprocess.run(
        "allure generate ./report -o ./new_report",
        cwd=project_dir,
        shell=True,
        check=True,
    )
    print("查看报告：allure open ./new_report")


if __name__ == "__main__":
    main()
