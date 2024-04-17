#!/usr/bin/python3
"""
Utility functions for clearing the contents of a txt stream
"""
import os
from typing import TextIO
from models.engine.file_storage import FileStorage


def clear_stream(stream: TextIO):
    """clears the contents of a given stream, which is
    a text stream e.g file stream opened in text mode
    Args: stream (TextIO): The stream to clear
    """
    # means you can mv the current file pointer
    # within the within the stream (seekable explanation)
    if stream.seekable():
        stream.seek(0)  # moves file ptr to begining of stream
        stream.truncate(0)  # clears stram contents


def delete_file(file_path: str):
    """Removes a file if it exists'
    file_path (str): The name of the file to remove
    """
    if os.path.isfile(file_path):
        os.unlink(file_path)


def reset_store(store: FileStorage, file_path='file.json'):
    """Resets the items in the given store
    store (FileStorage): The fileStorage to reset
    file_path (str): The path to store's file
    """
    with open(file_path, mode='w') as file:
        file.write('{}')
        if store is not None:
            store.reload()


def read_text_file(file_name):
    """Read the contents of a given file
    file_name (str): The name of the file to read
    Returns the contents of the file if it exists
    """
    lines = []
    if os.path.isfile(file_name):
        with open(file_name, mode='r') as file:
            for line in file.readlines():
                lines.append(line)
    return ''.join(lines)


def write_text_file(file_name, text):
    """Writes a text to a given file
    file_name (str): The name of the file to write to
    text (str): The content of the file
    """
    with open(file_name, mode='w') as file:
        file.write(text)
