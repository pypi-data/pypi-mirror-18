# -*- coding: utf-8 -*-

import os
import re
import shutil
import zipfile

import click
import mistune
import paramiko
import yaml
from jinja2 import Environment, FileSystemLoader

import blogbook.build.process
import blogbook.build.watch
import blogbook.constant
import blogbook.repo.push
import blogbook.serve
import blogbook.toolbox.file


@click.group()
@click.version_option('1.0')
def main():
    pass


@main.command()
@click.argument(
    'directory', required=False,
    default=os.getcwd()
)
@click.option(
    '-f', '--force',
    is_flag=True,
    help='Force override existing directory'
)
@click.option(
    '-l', '--layout',
    default=os.path.join(blogbook.constant.BUILTIN_LAYOUT_PATH, 'default'),
    metavar='PATH',
    help='The blogbook template path.'
)
def new(directory, force, layout):
    """
    Create a new blogbook.
    """

    if os.path.isdir(directory) and not blogbook.toolbox.file.is_empty(directory) and not force:
        raise click.UsageError(
            directory + ' already exist and is not an empty directory, '
            + 'either user an other directory or use the --force flag.'
        )

    if not os.path.isdir(layout) and not zipfile.is_zipfile(layout):
        raise click.BadParameter('You must provide either an existing layout directory or zip file')

    click.echo('Create new blogbook into [{}]'.format(directory))
    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)

    logbook_work_path = os.path.join(directory, blogbook.constant.LOGBOOK_DIRECTORY)
    blogbook.toolbox.file.force_mkdir(logbook_work_path)
    with open(os.path.join(logbook_work_path, 'version'), 'w') as stream_logbook:
        stream_logbook.write('0')

    click.echo('with layouts [{}]'.format(os.path.basename(layout)))
    layout_path = os.path.join(directory, blogbook.constant.LAYOUTS_DIRECTORY)
    if os.path.isdir(layout_path):
        shutil.rmtree(layout_path)

    if os.path.isdir(layout):
        shutil.copytree(layout, layout_path)
    elif zipfile.is_zipfile(layout):
        with zipfile.ZipFile(layout) as zf:
            zf.extractall(layout_path)


@main.command()
@click.option(
    '-s', '--source',
    default=os.getcwd(),
    metavar='PATH',
    help='The blogbook source path.'
)
@click.option(
    '-o', '--output',
    default=os.path.join(os.getcwd(), blogbook.constant.DEFAULT_OUTPUT),
    metavar='PATH',
    help='The blogbook output build path.'
)
@click.option(
    '-w', '--watch',
    is_flag=True,
    help='Build on change and run server.'
)
def build(source, output, watch):
    """
    Build a blogbook from his template.
    """

    context = {
        'setting': {
            'language': 'en',
            'name': os.path.basename(source),
            'content_exclude_patterns': ['_*', '.*'],
            'default_layout': 'post',
            'layouts_path': os.path.join(source, blogbook.constant.LAYOUTS_DIRECTORY),
            'excerpt_separator': '\n'
        },
        'site': {
            'index': [
                {
                    'layout': 'index',
                    'url': '/',
                    'title': 'index',
                    'content': {
                        'output_dir': output,
                        'output_path': os.path.join(output, 'index')
                    }
                }
            ]
        }
    }
    setting_path = os.path.join(source, blogbook.constant.LOGBOOK_DIRECTORY, 'setting.yml')
    if os.path.isfile(setting_path):
        with open(setting_path, 'r') as stream:
            context['setting'].update(yaml.safe_load(stream))

    context['setting']['content_exclude_patterns'] = [
        re.compile(content_exclude_pattern.replace('.', '\.').replace('*', '.*'))
        for content_exclude_pattern in context['setting']['content_exclude_patterns']
    ]

    layout_path = context['setting']['layouts_path']

    if not os.path.isdir(layout_path) or blogbook.toolbox.file.is_empty(layout_path):
        raise click.UsageError('Missing layout into ' + layout_path)

    blogbook.toolbox.file.force_mkdir(output)

    assets_path = os.path.join(layout_path, blogbook.constant.ASSETS_DIRECTORY)
    if os.path.isdir(assets_path) and not blogbook.toolbox.file.is_empty(assets_path):
        shutil.copytree(assets_path, os.path.join(output, blogbook.constant.ASSETS_DIRECTORY))

    markdown = mistune.Markdown()

    blogbook.build.process.pre_process(source, output, context, markdown)

    environment = Environment(loader=FileSystemLoader(context['setting']['layouts_path']))
    for pages in context['site'].values():
        for page in pages:
            blogbook.build.process.post_process_dynamic(page, context, markdown, environment)

    if watch:
        watcher = blogbook.build.watch.LogbookContentWatcher(source, output, context, markdown, environment)
        try:
            blogbook.serve.run_server(output, 1234)
        except KeyboardInterrupt:
            watcher.stop()


@main.command()
@click.option(
    '-r', '--root',
    default=os.path.join(os.getcwd(), blogbook.constant.DEFAULT_OUTPUT),
    metavar='PATH',
    help='The blogbook generated site path.'
)
@click.option(
    '-p', '--port',
    default=1234,
    metavar='PORT',
    help='Port on which binding the server.'
)
def serve(root, port):
    """
    Serve a blogbook generated content for test purpose only.
    """
    blogbook.serve.run_server(root, port)


@main.command()
@click.option(
    '-s', '--source',
    default=os.getcwd(),
    metavar='PATH',
    help='The blogbook source path.'
)
def push(source):
    """
    Serve a blogbook generated content for test purpose only.
    """

    setting = {}
    setting_path = os.path.join(source, blogbook.constant.LOGBOOK_DIRECTORY, 'setting.yml')
    if os.path.isfile(setting_path):
        with open(setting_path, 'r') as stream:
            setting = yaml.safe_load(stream)

    if 'remote' not in setting:
        raise click.UsageError('Missing remote setting')

    client = paramiko.SSHClient()
    client.load_host_keys(blogbook.constant.SSH_HOST_KEYS)
    client.set_missing_host_key_policy(blogbook.repo.push.ConfirmAddPolicy())

    client.connect(setting['remote']['host'])

    remote_root = '/var/www/blogbook/' + os.path.basename(source)
    client.exec_command('rm -rf {}'.format(remote_root))
    client.exec_command('mkdir -p {}'.format(remote_root))

    sftp = client.open_sftp()
    for local_root, dir_names, file_names in os.walk(source):

        current_remote_root = remote_root
        relative_path = os.path.relpath(local_root, source)
        if relative_path != os.curdir:
            current_remote_root += '/' + relative_path.replace('\\', '/')

        for file_name in file_names:
            local_file_path = os.path.join(local_root, file_name)
            remote_file_path = current_remote_root + '/' + file_name
            click.echo('{} --> {}'.format(local_file_path, remote_file_path))
            sftp.put(local_file_path, remote_file_path)
        for dir_name in dir_names:
            remote_dir_path = current_remote_root + '/' + dir_name
            click.echo('{} --> {}'.format(os.path.join(local_root, dir_name), remote_dir_path))
            sftp.mkdir(remote_dir_path)

    client.close()


if __name__ == "__main__":
    main()
