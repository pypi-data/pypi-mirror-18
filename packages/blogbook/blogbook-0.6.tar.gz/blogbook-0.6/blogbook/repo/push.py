# -*- coding: utf-8 -*-

import click
import paramiko

import blogbook.constant


class ConfirmAddPolicy(paramiko.MissingHostKeyPolicy):
    """
    Policy for confirm before adding the hostname and new host key to the
    local `.HostKeys` object, and saving it.  This is used by `.SSHClient`.
    """

    def missing_host_key(self, client, hostname, key):

        click.echo('The authenticity of host \'{}\' can\'t be established.'.format(hostname))
        click.echo(
            'RSA key fingerprint is MD5:{}.'.format(
                ''.join(format(x, '02x') for x in key.get_fingerprint())
            )
        )

        if click.confirm('Are you sure you want to continue connecting?'):
            client.get_host_keys().add(hostname, key.get_name(), key)
            client.save_host_keys(blogbook.constant.SSH_HOST_KEYS)
            click.echo('Warning: Permanently added \'{}\' (RSA) to the list of known hosts.'.format(hostname))
        else:
            raise paramiko.SSHException('Host key verification failed.')
