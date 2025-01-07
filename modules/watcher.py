from time import sleep
from typing import Any

from watchdog.events import FileSystemEventHandler, DirModifiedEvent, FileModifiedEvent, DirCreatedEvent, \
	FileCreatedEvent
from watchdog.observers import Observer
from modules.custom_print import print_info


class ChangeHandler(FileSystemEventHandler):
	def __init__(self, options: dict[str, Any]):
		super().__init__()
		self.is_updating = False
		self.options = options

	def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
		from main import parse_files
		if self.is_updating:
			return
		sleep(0.3)
		if self.is_updating:
			return

		if not event.is_directory:
			print_info(f"File {event.src_path} modified. Recompiling...")
			self.is_updating = True
			parse_files(self.options)
			self.is_updating = False


def watch(path: str, options: dict[str, Any]):
	handler = ChangeHandler(options)
	observer = Observer()
	observer.schedule(handler, path, recursive=True)
	observer.start()

	try:
		while True:
			sleep(1)
	except KeyboardInterrupt:
		observer.stop()

	observer.join()
