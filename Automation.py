import os
import sys
from os import scandir, rename
from os import splitext, exist, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

source_dir = r"C:\Users\aayus\Downloads"
target_dir_images = r"C:\Users\aayus\Downloads\Downloaded Images"
target_dir_videos = r"C:\Users\aayus\Downloads\Downloaded Videos"
target_dir_music = r"C:\Users\aayus\Downloads\Downloaded Music"
target_dir_doc = r"C:\Users\aayus\Downloads\Downloaded Documents"
target_dir_pro = r"C:\Users\aayus\Downloads\Downloaded Set Up files"

image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]

video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]

document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exist(f"./{dest}/{name}"):
        name = f"./{dest}/{name}"
        counter +=1
    return name

def move_files(dest, entry, name):
    if exists(f"./{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldname = join(dest, name)
        newname = join(dest, unique_name)
        rename(oldname, newname)
    move(entry, dest)

class MoveHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir("source_dir") as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)

    def check_audio_files(self, entry, name):
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
              move_files(target_dir_music, entry, name)
                logging.info(f"Moved audio file: {name}")


    def check_video_files(self, entry, name):
        for video_extension in audio_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_files(target_dir_videos, entry, name)
                logging.info(f"Moved video file: {name}")


    def check_document_files(self, entry, name):
        for document_extension in document_extensions:
            if name.endswith(document_extension) or name.endswith(document_extension.upper()):
                move_files(target_dir_doc, entry, name)
                logging.info(f"Moved document file: {name}")

    def check_image_files(self, entry, name):
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_files(target_dir_images, entry, name)
                logging.info(f"Moved image file: {name}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

