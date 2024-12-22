import json
import difflib


def generate_diff_json(file1_path, file2_path):
    with open(file1_path, "r", encoding="utf-8") as file1, open(
        file2_path, "r", encoding="utf-8"
    ) as file2:
        content1 = file1.readlines()
        content2 = file2.readlines()

    differ = difflib.Differ()
    diff = list(differ.compare(content1, content2))

    diff_json = []

    for line in diff:
        if line.startswith("+ "):
            diff_json.append({"type": "added", "content": line[2:].strip()})
        elif line.startswith("- "):
            diff_json.append({"type": "removed", "content": line[2:].strip()})
        else:
            diff_json.append({"type": "unchanged", "content": line[2:].strip()})

    return diff_json


def save_diff_json(diff_json, output_path):
    with open(output_path, "w", encoding="utf-8") as output_file:
        json.dump(diff_json, output_file, indent=4)


# file1_path = "sample_pdfs/old_version.md"  # Path to the first markdown file
# file2_path = "sample_pdfs/new_version.md"  # Path to the second markdown file
# output_json_path = "sample_pdfs/diff_output.json"  # Path to save the JSON diff

# diff_json = generate_diff_json(file1_path, file2_path)
# save_diff_json(diff_json, output_json_path)

# print(f"Differences saved as JSON to {output_json_path}")
