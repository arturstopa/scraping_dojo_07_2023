import os
import subprocess

from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    output_file = os.getenv("OUTPUT_FILE")

    PROJECT_DIR = "sigmoidal"
    subprocess.run(["scrapy", "startproject", PROJECT_DIR])
    cwd = os.getcwd()
    os.chdir(PROJECT_DIR)
    subprocess.run(["scrapy", "crawl", "quotes", "-o", f"../{output_file}"])
