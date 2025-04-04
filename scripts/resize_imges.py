from PIL import Image


# Function to downsize an image
def downsize_image(input_path, output_path, max_width, max_height):
    with Image.open(input_path) as img:
        # Maintain aspect ratio
        img.thumbnail((max_width, max_height), Image.LANCZOS)
        img.save(output_path, format="PNG", optimize=True)
        print(f"Image saved to {output_path}")


downsize_image(
    "/home/diego/Downloads/EU_response.jpg",
    "/home/diego/Downloads/EU_response_r.jpg",
    max_width=200,
    max_height=200,
)
