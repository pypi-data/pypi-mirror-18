# -*- coding: utf-8 -*-

import datetime
import os
import shutil
import urllib.request

import click
import yaml
from jinja2 import TemplateNotFound

import blogbook.constant
import blogbook.toolbox.file


def pre_process_dynamic(file_path, filename, output_dir, setting, markdown, base_path):
    relative_path = os.path.relpath(blogbook.toolbox.file.parentdir(file_path), base_path)
    base_url = blogbook.constant.URL_SEPARATOR
    if relative_path != os.path.curdir:
        base_url += urllib.request.pathname2url(relative_path) + blogbook.constant.URL_SEPARATOR

    filename_pattern = blogbook.constant.FILENAME_REGEX.match(filename)
    output_name = filename_pattern.group(5)

    page = {
        'layout': setting['default_layout'],
        'url': base_url + output_name,
        'title': output_name.capitalize(),
        'excerpt_separator': setting['excerpt_separator']
    }
    if filename_pattern.group(2) and filename_pattern.group(3) and filename_pattern.group(4):
        year = int(filename_pattern.group(2))
        month = int(filename_pattern.group(3))
        day = int(filename_pattern.group(4))
        page['date'] = datetime.date(year, month, day)

    with open(file_path, 'r') as stream:

        line = ''
        content_position = 0
        for line in stream:
            if line.strip():
                break
            content_position += len(line) + 1

        if line.strip() == '---':

            content_position += len(line) + 1
            is_meta_close = False
            meta = ''
            for line in stream:
                content_position += len(line) + 1
                is_meta_close = (line.strip() == '---')
                if is_meta_close:
                    break
                meta += line

            if not is_meta_close:
                raise click.UsageError(
                    'Meta section open but never close on content file [{}]'.format(filename)
                )

            page.update(yaml.safe_load(meta))

            for line in stream:
                if line.strip():
                    break
                content_position += len(line) + 1

        if 'excerpt' not in page:

            excerpt = line
            is_excerpt_close = False
            for line in stream:
                is_excerpt_close = line == page['excerpt_separator']
                if is_excerpt_close:
                    page['excerpt'] = excerpt
                    break
                excerpt += line

            if not is_excerpt_close:
                page['excerpt'] = excerpt

        page['excerpt'] = markdown(page['excerpt'])

    page['content'] = {
        'path': file_path,
        'position': content_position,
        'output_dir': output_dir,
        'output_path': os.path.join(output_dir, output_name)
    }

    return page


def process_static(file_path, output_dir):
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    shutil.copy(file_path, output_dir)


def pre_process(path, output_dir, context, markdown, base_content_path=None):
    """
    Scan source directory in order to :
        - Copy any file other than content file (*.md) into destination directory.
        - Parse content file to populate site dictionary context.
    """
    base_content_path = base_content_path if base_content_path else path

    for entry in os.scandir(path):

        if entry.is_dir():
            pre_process(
                entry.path,
                os.path.join(output_dir, entry.name),
                context,
                markdown,
                base_content_path
            )

        elif entry.is_file():

            if entry.name.lower().endswith(blogbook.constant.MARKDOWN_EXT):

                page = pre_process_dynamic(
                    entry.path, entry.name, output_dir, context['setting'], markdown, base_content_path
                )

                layout_group = page['layout'] + 's'
                if layout_group in context['site']:
                    context['site'][layout_group].append(page)
                else:
                    context['site'][layout_group] = [page]

            else:
                process_static(entry.path, output_dir)


def post_process_dynamic(page, context, markdown, environment):
    """
    Scan site dictionary context in order to generate static html page
    base on site setting, template and page content.
    """

    output_dir = page['content']['output_dir']
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(page['content']['output_path'], 'w') as output_stream:

        context['page'] = page

        with open(page['content']['path'], 'r') as source_stream:
            source_stream.seek(page['content']['position'])
            context['content'] = markdown(source_stream.read())

        try:
            output_stream.write(
                environment.get_template(page['layout'] + blogbook.constant.LAYOUT_EXT).render(context)
            )
        except TemplateNotFound as ex:
            raise click.UsageError('Missing required layout : {}'.format(ex.message))

        del context['content']
