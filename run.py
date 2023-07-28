import os
import subprocess

from dotenv import load_dotenv


def start_project(project_dir: str):
    result = subprocess.run(["scrapy", "startproject", project_dir])
    print(result)


if __name__ == "__main__":
    load_dotenv()
    output_file = os.getenv("OUTPUT_FILE")

    PROJECT_DIR = "sigmoidal"
    start_project(PROJECT_DIR)
    cwd = os.getcwd()
    os.chdir(PROJECT_DIR)
    subprocess.run(["scrapy", "crawl", "quotes", "-o", f"../{output_file}"])
