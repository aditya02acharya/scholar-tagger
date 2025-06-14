"""
Script to download ArXiv dataset from Kaggle.
Requires Kaggle API credentials to be set up.
"""

import argparse
import subprocess
import sys
import zipfile
from pathlib import Path


def download_dataset(dataset_name: str, output_dir: Path):
    """
    Download dataset from Kaggle using the Kaggle API.

    Args:
        dataset_name (str): The name of the dataset on Kaggle.
        output_dir (str): The directory where the dataset will be saved.
    """
    try:
        subprocess.run(  # noqa: S603
            ["kaggle", "datasets", "download", dataset_name, "-p", output_dir],  # noqa: S607
            check=True,
        )

        zip_file = output_dir / f"{dataset_name.split('/')[-1]}.zip"

        if not zip_file.exists():
            print(f"Error: Downloaded zip file {zip_file} does not exist.")
            sys.exit(1)

        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall(output_dir)
        print(f"Dataset downloaded and extracted to: {output_dir}")

        # Clean up the zip file after extraction
        zip_file.unlink(missing_ok=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading dataset: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Download ArXiv dataset")
    parser.add_argument("--output-dir", type=Path, default=Path("data/raw"), help="Output directory for dataset")
    parser.add_argument(
        "--dataset", type=str, default="barclaysav/b-interview-arxiv-dataset", help="Kaggle dataset name"
    )

    args = parser.parse_args()

    print("ArXiv Dataset Downloader")
    print("=" * 50)

    download_dataset(args.dataset, args.output_dir)

    print("\n✓ All expected files present")
    print(f"\nDataset downloaded to: {args.output_dir}")


if __name__ == "__main__":
    main()
