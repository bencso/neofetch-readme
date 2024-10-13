from PIL import Image, ImageOps
import numpy as np

class Bio:
    def __init__(self):
        self.name = self.get_non_empty_input("Enter your name: ")
        self.age = self.get_valid_age("Enter your age: ")
        self.occupation = self.get_non_empty_input("Enter your occupation: ")
        self.location = self.get_non_empty_input("Enter your location: ")
        self.interests = self.get_non_empty_input("Enter your interests (comma-separated): ").split(", ")
        self.languages = self.get_languages()
        self.technologies = self.get_technologies()
        self.frameworks = self.get_non_empty_input("Enter the frameworks you are learning (comma-separated): ").split(", ")
        self.tools = self.get_non_empty_input("Enter the tools you use (comma-separated): ").split(", ")
        self.bio_info = self.generate_bio_info()

    def get_non_empty_input(self, prompt):
        while True:
            value = input(prompt)
            if value.strip():
                return value
            print("This field cannot be empty. Please enter a valid value.")

    def get_valid_age(self, prompt):
        while True:
            try:
                age = int(input(prompt))
                if age > 0:
                    return age
                else:
                    print("Age must be a positive number.")
            except ValueError:
                print("Please enter a valid number for age.")

    def get_languages(self):
        languages = {}
        while True:
            lang = input("Enter a language you know (or 'done' to finish): ")
            if lang.lower() == 'done':
                break
            if lang.strip():
                level = self.get_non_empty_input(f"Enter your proficiency level in {lang}: ")
                languages[lang] = level
            else:
                print("Language cannot be empty.")
        return languages

    def get_technologies(self):
        technologies = {}
        while True:
            tech_type = input("Enter a technology type (e.g., Languages, Databases, Web) (or 'done' to finish): ")
            if tech_type.lower() == 'done':
                break
            if tech_type.strip():
                tech_list = self.get_non_empty_input(f"Enter the technologies for {tech_type} (comma-separated): ").split(", ")
                technologies[tech_type] = tech_list
            else:
                print("Technology type cannot be empty.")
        return technologies

    def generate_bio_info(self):
        bio_info = [
            f"Name: {self.name}",
            f"Age: {self.age}",
            f"Occupation: {self.occupation}",
            f"Location: {self.location}",
            f"Interests: {', '.join(self.interests)}",
            f"Languages:",
        ] + [f"  - {key}: {value}" for key, value in self.languages.items()] + [
            f"Technologies:",
        ] + [f"  - {key}: {', '.join(value)}" for key, value in self.technologies.items()] + [
            f"Frameworks:",
        ] + [f"  - {framework}" for framework in self.frameworks] + [
            f"Tools: {', '.join(self.tools)}"
        ]
        return bio_info

class CreateText:
    def __init__(self, image_path, ascii_chars):
        self.image_path = image_path
        self.ascii_chars = ascii_chars
        self.image = Image.open(self.image_path)
        self.image = self.crop_image(self.image)
        self.image_gray = self.image.convert("L")
        self.image_small = self.image_gray.resize((50, 30))
        self.pixels = np.array(self.image_small)
        
    def crop_image(self, image):
        return ImageOps.crop(image, border=0)
        
    def convert_image_to_ascii(self):
        ascii_image = "\n".join(
            "".join(self.ascii_chars[min(pixel // (256 // len(self.ascii_chars)), len(self.ascii_chars) - 1)] for pixel in row) for row in self.pixels
        )
        return ascii_image.strip()
    
    def format_ascii_image(self, ascii_image):
        ascii_lines = ascii_image.split("\n")
        ascii_lines = [line.strip() for line in ascii_lines]
        max_len = max(len(line) for line in ascii_lines)
        ascii_lines = [line.ljust(max_len) for line in ascii_lines]
        return ascii_lines
    
    def combine_ascii_and_bio(self, ascii_lines, info_lines):
        total_lines = len(ascii_lines)
        bio_lines = len(info_lines)
        padding_top = (total_lines - bio_lines) // 2
        padding_bottom = total_lines - bio_lines - padding_top
        padded_info_lines = [""] * padding_top + info_lines + [""] * padding_bottom
        combined_output = "\n".join(
            f"{ascii_line}  {info_line}" for ascii_line, info_line in zip(ascii_lines, padded_info_lines)
        )
        return combined_output
    
    def save_output_to_file(self, output, filename):
        with open(filename, "w") as file:
            file.write(output)
            
    def generate_final_output(self, ascii_lines, info_lines):
        combined_output = self.combine_ascii_and_bio(ascii_lines, info_lines)
        return combined_output
    
    def main(self):
        ascii_image = self.convert_image_to_ascii()
        ascii_lines = self.format_ascii_image(ascii_image)
        return ascii_lines
        
image_path = input("Enter the path to the image file (path/filename.ext): ")
while True:
    ascii_chars = f" {input('Enter the ASCII characters to use (3 characters):')}"
    if len(ascii_chars) == 4:
        break
    print("Please enter exactly 3 characters.")
# Bio
bio = Bio()
info_lines = bio.bio_info
# Image to ASCII
create_text = CreateText(image_path, ascii_chars)
ascii_lines = create_text.main()
# Combine ASCII and Bio
combined_output = create_text.combine_ascii_and_bio(ascii_lines, info_lines)
# Save to file
create_text.save_output_to_file(combined_output, "ascii_image.txt")
