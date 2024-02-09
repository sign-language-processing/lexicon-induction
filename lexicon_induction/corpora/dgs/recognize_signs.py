import math
from pathlib import Path
from pose_format import Pose

from lexicon_induction.corpora.dgs.dgs_utils import get_elan_sentences
from sign_language_recognition.kaggle_asl_signs import predict

# from sign_language_datasets.datasets.dgs_corpus.dgs_utils import get_elan_sentences


# Path to the segmentation directory
segments_dir = Path('segments')


def load_pose(pose_path: Path):
    if not pose_path.exists():
        return None

    with open(pose_path, "rb") as f:
        buffer = f.read()
        return Pose.read(buffer)


def process_segment_files():
    """Process each EAF file in the segmentation directory."""
    for eaf_file in segments_dir.glob('*.eaf'):
        # Call the get_elan_sentences function on each file
        sentences = list(get_elan_sentences(str(eaf_file)))

        # Assuming the eaf_file is a Path object
        file_stem = eaf_file.stem  # This gets the file name without the extension

        # Constructing the paths for the _a and _b pose files
        pose_a = load_pose(eaf_file.parent.parent / f"poses/{file_stem}_a.pose")
        pose_b = load_pose(eaf_file.parent.parent / f"poses/{file_stem}_b.pose")

        # You can process the sentences as needed
        # For example, print them or store them
        print(f"Sentences in {eaf_file.name}: {len(sentences)}")
        for sentence in sentences:
            pose = pose_a if sentence['participant'] == 'A' else pose_b
            for gloss in sentence['glosses']:
                start_frame = int(gloss["start"] / 1000 * pose.body.fps)
                end_frame = math.ceil(gloss["end"] / 1000 * pose.body.fps)

                cropped_pose = Pose(
                    header=pose.header,
                    body=pose.body[start_frame:end_frame]
                )
                vector = predict(cropped_pose)
                print(vector)
                # with open("test.pose", "wb") as f:
                #     cropped_pose.write(f)
                #     exit()


# Process the segment files
process_segment_files()
