# -*- coding: utf-8 -*-

import os
import shutil
import threading
import time

import click
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import blogbook.build.process
import blogbook.constant
import blogbook.toolbox.collection
import blogbook.toolbox.file


class ContentEventHandler(FileSystemEventHandler):
    def __init__(self, builder):
        self.builder = builder
        builder.start()

    def on_any_event(self, event):
        super(ContentEventHandler, self).on_moved(event)

        if not event.is_directory or event.event_type == 'deleted':
            if event.event_type == 'created':
                event.event_type = 'modified'
            self.builder.add(event)


class LogbookEventBuilder(threading.Thread):
    def __init__(self, content_path, output_path, context, markdown, environment):
        threading.Thread.__init__(self)
        self._event_queue = blogbook.toolbox.collection.SetQueue()
        self._content_path = content_path
        self._output_path = output_path
        self._context = context
        self._markdown = markdown
        self._environment = environment

    def add(self, event):
        self._event_queue.put(event)

    def run(self):

        while True:
            try:
                event = self._event_queue.peek()

                source_content_relative_path = os.path.relpath(event.src_path, self._content_path)
                source_output_path = os.path.join(self._output_path, source_content_relative_path)
                source_output_dir = blogbook.toolbox.file.parentdir(source_output_path)
                source_content_name = os.path.basename(event.src_path)

                if event.src_path.lower().endswith(blogbook.constant.MARKDOWN_EXT):

                    if event.event_type in ['created', 'modified']:

                        click.echo("{} content: {}".format(event.event_type.capitalize(), source_output_path))
                        page = blogbook.build.process.pre_process_dynamic(
                            event.src_path,
                            source_content_name,
                            source_output_dir,
                            self._context['setting'],
                            self._markdown,
                            self._content_path
                        )

                        layout_group = page['layout'] + 's'
                        if layout_group in self._context['site']:

                            update = False
                            for i, layout_page in enumerate(self._context['site'][layout_group]):
                                update = layout_page['content']['path'] == event.src_path
                                if update:
                                    self._context['site'][layout_group][i] = page
                                    break
                            if not update:
                                self._context['site'][layout_group].append(page)

                        else:
                            self._context['site'][layout_group] = [page]

                        blogbook.build.process.post_process_dynamic(
                            page, self._context, self._markdown, self._environment
                        )

                    elif event.event_type == 'moved':
                        # TODO : Handle content rename (aka. move)
                        pass

                    elif event.event_type == 'deleted':

                        for layout_group, pages in self._context['site'].items():
                            for i, page in enumerate(pages):
                                if page['content']['path'] == event.src_path:
                                    blogbook.toolbox.file.silently_remove(page['content']['output_path'])
                                    del self._context['site'][layout_group][i]
                                    break

                    for index in self._context['site']['indexs']:
                        blogbook.build.process.post_process_dynamic(
                            index, self._context, self._markdown, self._environment
                        )

                else:

                    if event.event_type in ['created', 'modified']:

                        click.echo("{} file: {}".format(event.event_type.capitalize(), source_output_path))
                        blogbook.build.process.process_static(event.src_path, source_output_dir)

                    elif event.event_type == 'moved':

                        destination_content_relative_path = os.path.relpath(event.dest_path, self._content_path)
                        destination_output_path = os.path.join(self._output_path, destination_content_relative_path)
                        destination_output_dir = blogbook.toolbox.file.parentdir(destination_output_path)

                        if not os.path.isdir(destination_output_dir):
                            os.makedirs(destination_output_dir, exist_ok=True)

                        click.echo("Moved file: from {} to {}".format(source_output_path, destination_output_path))
                        shutil.move(source_output_path, destination_output_path)

                        if blogbook.toolbox.file.is_empty(source_output_dir):
                            blogbook.toolbox.file.silently_rmdir(source_output_dir)

                    elif event.event_type == 'deleted':

                        if os.path.isdir(source_output_path):
                            click.echo("Deleted directory: {}".format(source_output_path))
                            shutil.rmtree(source_output_path)
                        else:
                            click.echo("Deleted file: {}".format(source_output_path))
                            blogbook.toolbox.file.silently_remove(source_output_path)

                        if blogbook.toolbox.file.is_empty(source_output_dir):
                            blogbook.toolbox.file.silently_rmdir(source_output_dir)

            except Exception as ex:
                click.echo('Error {} : {}'.format(type(ex), ex))

            time.sleep(1)
            self._event_queue.get()


class LogbookContentWatcher(object):
    def __init__(self, content_path, output_path, context, markdown, environment):
        builder = LogbookEventBuilder(content_path, output_path, context, markdown, environment)
        self.observer = Observer()
        self.observer.schedule(ContentEventHandler(builder), content_path, recursive=True)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()
