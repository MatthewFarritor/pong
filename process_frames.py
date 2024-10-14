import os
from PIL import Image
import imagehash
import pygame

pygame.init()

FRAMES_FOLDER = 'Frames'
SECTIONS_FOLDER = 'Sections'

if not os.path.exists(SECTIONS_FOLDER):
    os.makedirs(SECTIONS_FOLDER)

def process_unique_sections():
    frame_files = [f for f in os.listdir(FRAMES_FOLDER) if f.endswith('.png')]
    frame_files.sort()
    frame_files = frame_files[:234164]

    section_width = 25
    section_height = 25

    saved_sections = set()
    processed_frames = 0

    for frame_file in frame_files:
            frame_path = os.path.join(FRAMES_FOLDER, frame_file)

            frame_image = Image.open(frame_path)

            frame_surface = pygame.image.fromstring(
                 frame_image.tobytes(), frame_image.size, frame_image.mode
            )

            frame_width, frame_height = frame_surface.get_size()

            frame_name = os.path.splitext(frame_file)[0]
            frame_number = frame_name.split('_')[1]


            for y in range(0, frame_height,section_height):
                 for x in range(0, frame_width,section_width):
                    rect = pygame.Rect(x, y, section_width, section_height)

                    section_surface = pygame.Surface((section_width, section_height))

                    section_surface.blit(frame_surface, (0, 0), rect)
                    
                    section_data = pygame.image.tostring(section_surface, "RGB")
                    section_image = Image.frombytes("RGB", (section_width, section_height), section_data)

                    section_hash = imagehash.average_hash(section_image)

                    if section_hash in saved_sections:
                         continue
                    
                    saved_sections.add(section_hash)

                    section_filename = os.path.join(
                           SECTIONS_FOLDER,
                           f'section_frame{frame_number}_x{x}_y{y}.png'
                      )

                    section_image.save(section_filename)

            processed_frames += 1 
            print(f'Processed frame {frame_number}')

    print(f'Total frames processed: {processed_frames}')
    print(f'Total unique sections saved: {len(saved_sections)}')
    
    pygame.quit()

if __name__ == '__main__':
    process_unique_sections()
