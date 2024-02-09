import json
from pathlib import Path
import requests

from tqdm import tqdm

# Assuming you have your JSON data in a file named 'dataset.json'
dataset_file = 'dataset.json'

# Directories for saving files
segments_dir = Path('segments')
poses_dir = Path('poses')

# Create directories if they don't exist
segments_dir.mkdir(parents=True, exist_ok=True)
poses_dir.mkdir(parents=True, exist_ok=True)


def download_file(url, path):
    if path.exists():
        return

    """Download a file from a URL to a given path."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download {url}")


def process_dataset(json_data):
    """Process each entry in the dataset JSON."""
    for key, value in tqdm(json_data.items()):
        # Download EAF file
        eaf_url = value.get('eaf')
        if eaf_url:
            eaf_file = segments_dir / f"{key}.eaf"
            download_file(eaf_url, eaf_file)

        # Download Holistic A file
        holistic_a_url = value.get('holistic_a')
        if holistic_a_url:
            holistic_a_file = poses_dir / f"{key}_a.pose"
            download_file(holistic_a_url, holistic_a_file)

        # Download Holistic B file
        holistic_b_url = value.get('holistic_b')
        if holistic_b_url:
            holistic_b_file = poses_dir / f"{key}_b.pose"
            download_file(holistic_b_url, holistic_b_file)


# Load JSON data
with open(dataset_file, 'r') as file:
    data = json.load(file)

# Process the dataset
process_dataset(data)
