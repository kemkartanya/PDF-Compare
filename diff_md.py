import difflib


def create_markdown_file(file_name, document):
    with open(file_name, "w") as file:
        file.write(document[0].text)


def generate_diff(file1_path, file2_path):
    with open(file1_path, "r", encoding="utf-8") as file1, open(
        file2_path, "r", encoding="utf-8"
    ) as file2:
        content1 = file1.readlines()
        content2 = file2.readlines()

    differ = difflib.Differ()
    diff = list(differ.compare(content1, content2))

    highlighted_diff = []

    for line in diff:
        if line.startswith("+ "):
            # Added text: Highlight in green
            highlighted_diff.append(f'<span style="color: green;">{line[2:]}</span>')
        elif line.startswith("- "):
            # Removed text: Highlight in red
            highlighted_diff.append(f'<span style="color: red;">{line[2:]}</span>')
        else:
            # Unchanged text: Keep original formatting
            highlighted_diff.append(line[2:])

    return highlighted_diff


def save_highlighted_diff(highlighted_diff, output_path):
    with open(output_path, "w", encoding="utf-8") as output_file:
        for line in highlighted_diff:
            output_file.write(line)


# file1_path = "sample_pdfs/old_version.md"  # Path to the first markdown file
# file2_path = "sample_pdfs/new_version.md"  # Path to the second markdown file
# output_path = "sample_pdfs/highlighted_diff.md"  # Path to save the highlighted diff

# highlighted_diff = generate_diff(file1_path, file2_path)
# save_highlighted_diff(highlighted_diff, output_path)

# print(f"Highlighted differences saved to {output_path}")
