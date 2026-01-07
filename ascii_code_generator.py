def read_pgm_image(file_path):
    with open(file_path, "rb") as file:
        format_identifier = file.readline().decode("ascii").strip()

        while True:
            header_line = file.readline().decode("ascii")
            if not header_line.startswith("#"):
                break

        image_width, image_height = map(int, header_line.split())
        max_gray_value = int(file.readline().decode("ascii").strip())

        pixel_data = []
        for line in file:
            pixel_data.extend(map(int, line.split()))

        return image_width, image_height, max_gray_value, pixel_data


def calculate_terminal_dimensions(
        image_width, image_height, max_terminal_width=80
    ):
    aspect_ratio = image_height / image_width

    if image_width > max_terminal_width:
        output_width = max_terminal_width
        output_height = int(output_width * aspect_ratio * 0.5)
    else:
        output_width = image_width
        output_height = int(image_height * 0.5)

    return output_width, output_height


def convert_pgm_to_ascii(image_path, max_terminal_width=80):
    character_set="@%#*+=-:. "
    (
        image_width, image_height, 
        max_gray_value, pixel_data
    ) = read_pgm_image(image_path)

    output_width, output_height = calculate_terminal_dimensions(
        image_width, image_height, max_terminal_width
    )

    horizontal_step = image_width / output_width
    vertical_step = image_height / output_height

    ascii_matrix = []

    for row_index in range(output_height):
        row = []
        for column_index in range(output_width):
            source_x = int(column_index * horizontal_step)
            source_y = int(row_index * vertical_step)
            pixel_position = source_y * image_width + source_x

            normalized_intensity = pixel_data[pixel_position] / max_gray_value
            character_position = int(
                normalized_intensity * (len(character_set) - 1)
            )

            row.append(character_set[character_position])

        ascii_matrix.append(row)

    return ascii_matrix


def generate_ascii_program(ascii_matrix, output_file_path):
    total_rows = len(ascii_matrix)
    total_columns = len(ascii_matrix[0]) if total_rows else 0

    program_lines = []
    program_lines.append(f"for row_index in range({total_rows}):")
    program_lines.append(f"    for column_index in range({total_columns}):")

    for row in range(total_rows):
        for column in range(total_columns):
            character = ascii_matrix[row][column]

            if character == "\\":
                character = "\\\\"
            elif character == "'":
                character = "\\'"

            program_lines.append(
                f"        if row_index == {row} and column_index == {column}:"
            )
            program_lines.append(f"            print('{character}', end='')")

    program_lines.append("    print()")

    with open(output_file_path, "w") as output_file:
        output_file.write("\n".join(program_lines))


if __name__ == "__main__":
    input_image_path = "rajkapoor.pgm"
    output_script_path = "ascii_art_code.py"

    ascii_representation = convert_pgm_to_ascii(input_image_path)
    generate_ascii_program(ascii_representation, output_script_path)

    print("ASCII art code generation completed.")
    print(f"Output file: {output_script_path}")
