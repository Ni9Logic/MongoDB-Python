def center_text_between_lines(text):
    line_length = len(text) + 4  # Length of the line containing dashes, accounting for padding

    # Create the line of dashes
    line = '-' * line_length

    # Construct the centered text with lines
    centered_text = f"\t\t\t{line}\n\t\t\t\t{text}\n\t\t\t{line}"

    return centered_text
