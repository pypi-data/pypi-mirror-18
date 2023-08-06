#!/usr/bin/env python
# coding=utf-8
""" Integration and Unit tests for sshreader Python Package
"""
from __future__ import print_function
from builtins import range, str
import click
import json
import os
import sys
import unittest
import warnings

__author__ = 'Jesse Almanrode (jesse@almanrode.com)'
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
import sshreader


class TestShellScript(unittest.TestCase):
    """ Test Cases for the shell script portion of SSH module
    """

    def test_shell_command(self):
        """ Test shell_command method
        """
        result = sshreader.shell_command('echo "foo"')
        self.assertIsInstance(result, tuple)
        self.assertEqual(result.return_code, 0)
        self.assertEqual(result.stdout, 'foo')
        self.assertEqual(len(result.stderr), 0)
        pass

    def test_shell_command_combined(self):
        """ Test combining stdout and stderr of shell_command method
        """
        result = sshreader.shell_command('echo "foo"; echo "bar" 1>&2', combine=True)
        self.assertIsInstance(result, tuple)
        self.assertEqual(result.return_code, 0)
        pass

    def test_shell_command_stderr(self):
        """ Test stderr of shell_command method
        """
        result = sshreader.shell_command('echo "bar" 1>&2')
        self.assertIsInstance(result, tuple)
        self.assertEqual(result.return_code, 0)
        self.assertEqual(result.stderr, 'bar')
        pass

    def test_decode_bytes(self):
        """ Test to ensure that result is a unicode string type
        """
        result = sshreader.shell_command('uname -a', decodebytes=True)
        self.assertIsInstance(result.stdout, str)
        pass


class TestSSH(unittest.TestCase):
    """ Test cases for the SSH class
    """

    def setUp(self):
        """ Setup SSH connection
        :return: Connection state conn.is_alive()
        """
        global ssh_data
        self.conn = sshreader.SSH(ssh_data['host_fqdn'], username=ssh_data['ssh_user'],
                                  password=ssh_data['ssh_password'], connect=False)
        return self.conn.is_alive()

    def test_password(self):
        """ Test an SSH connection using a password
        """
        self.conn.connect()
        self.conn.is_alive()
        self.assertTrue(self.conn.is_alive(), msg='ssh connection using password failed to: ' + ssh_data['host_fqdn'])
        self.conn.close()
        pass

    def test_keyfile(self):
        """ Test an SSH connection using an ssh key
        """
        global ssh_data
        conn = sshreader.SSH(ssh_data['host_fqdn'], username=ssh_data['ssh_user'],
                             keyfile=ssh_data['ssh_public_key_path'])
        self.assertTrue(conn.is_alive(), msg='ssh connection using password failed to: ' + ssh_data['host_fqdn'])
        pass

    def test_reconnect(self):
        """ Test re-opening an SSH connection
        """
        self.assertFalse(self.conn.is_alive())
        self.conn.reconnect()
        self.assertTrue(self.conn.is_alive())
        pass

    def test_command(self):
        """ Test an ssh_command
        """
        self.assertFalse(self.conn.is_alive())
        self.conn.connect()
        result = self.conn.ssh_command('echo foo')
        self.assertIsInstance(result, tuple)
        self.assertEqual(result.return_code, 0)
        self.assertEqual(result.stdout, 'foo')
        pass

    def test_command_stderr(self):
        """ Test an ssh_command
        """
        self.assertFalse(self.conn.is_alive())
        self.conn.connect()
        result = self.conn.ssh_command('echo bar 1>&2')
        self.assertIsInstance(result, tuple)
        self.assertEqual(result.return_code, 0)
        self.assertEqual(result.stderr, 'bar')
        pass

    def test_combine_output(self):
        """ Test combining stdout and stderr of ssh_command
        """
        self.assertFalse(self.conn.is_alive())
        self.conn.connect()
        result = self.conn.ssh_command('echo foo; echo bar 1>&2;', combine=True)
        self.assertIsInstance(result, tuple)
        self.assertEqual(result.return_code, 0)
        self.assertEqual(result.stdout, 'foo\r\nbar')
        pass

    def test_cmd_timeout(self):
        """ Test handling of cmd timeout via SSH
        """
        if self.conn.is_alive() is False:
            self.conn.connect()
        self.assertTrue(self.conn.is_alive())
        result = self.conn.ssh_command('sleep 5', timeout=2)
        self.assertIsInstance(result, tuple)
        self.assertEqual(result.return_code, 124)
        self.assertIn('Command timed out', result.stderr)
        pass


def my_hook(*args):
    """ Function for testing hook
    :param args: Args should be ('pre|post', sshreader.ServerJob)
    :return:
    """
    args = list(args)
    if len(args) == 1:
        if args[0] in ('pre', 'post') and isinstance(args.pop(), sshreader.ServerJob):
            return True
        else:
            return False
    else:
        if args[0] in ('pre', 'post'):
            return True
        else:
            return False


class TestSshreader(unittest.TestCase):
    """ Test cases for the sshreader module
    """

    def configure_serverjob_list(self, size):
        """ Configure a list of serverjob objects to sshread (including pre and post hooks) and local commands
        :return: List
        """
        global ssh_data
        pre = sshreader.Hook(my_hook, args=['pre'])
        post = sshreader.Hook(my_hook, args=['post'])
        jobs = list()
        for x in range(size):
            jobs.append(sshreader.ServerJob(ssh_data['host_fqdn'], 'sleep 1', prehook=pre, posthook=post,
                                            username=ssh_data['ssh_user'], password=ssh_data['ssh_password']))
        for x in range(size):
            jobs.append(sshreader.ServerJob('local-' + str(x), 'sleep 1', runlocal=True))
        return jobs

    def test_Hook_creation(self):
        """ Test valid hook creation
        """
        myhook = sshreader.Hook(my_hook, args=['pre'])
        self.assertIsInstance(myhook, sshreader.Hook)
        pass

    def test_ServerJob(self):
        """ Test valid ServerJob creation
        """
        global ssh_data
        job = sshreader.ServerJob(ssh_data['host_fqdn'], 'echo foo',
                                  username=ssh_data['ssh_user'], password=ssh_data['ssh_password'])
        self.assertIsInstance(job, sshreader.ServerJob)
        pass

    def test_ServerJob_with_hooks(self):
        """ Test ServerJob with hooks
        """
        global ssh_data
        pre = sshreader.Hook(my_hook, args=['pre'])
        post = sshreader.Hook(my_hook, args=['post'])
        job = sshreader.ServerJob(ssh_data['host_fqdn'], 'echo foo', prehook=pre, posthook=post,
                                  username=ssh_data['ssh_user'], password=ssh_data['ssh_password'])
        self.assertIsInstance(job, sshreader.ServerJob)
        pass

    def test_sshread_threads(self):
        """ Test sshread method using threads
        """
        jobs = self.configure_serverjob_list(10)
        result = sshreader.sshread(jobs, tcount=0)
        for x in result:
            self.assertEqual(x.status, 0)
        pass

    def test_sshread_processes(self):
        """ Test sshread method using processes
        """
        jobs = self.configure_serverjob_list(10)
        result = sshreader.sshread(jobs, pcount=1)
        for x in result:
            self.assertEqual(x.status, 0)
        pass

    def test_sshread(self):
        """ Test sshread method using threads and processes
        """
        jobs = self.configure_serverjob_list(21)
        result = sshreader.sshread(jobs, pcount=0, tcount=0)
        for x in result:
            self.assertEqual(x.status, 0)
        pass

    def test_cpulimits(self):
        """ Ensure the cpulimit methods
        """
        self.assertIsInstance(sshreader.sshreader.cpusoftlimit(), int)
        self.assertIsInstance(sshreader.sshreader.cpuhardlimit(), int)
        pass


if __name__ == '__main__':
    global ssh_data
    try:
        params_file = open(project_root + '/test/test_params.json')
        ssh_data = json.load(params_file)
    except IOError:
        ssh_data = {'host_fqdn': None, 'ssh_user': None, 'ssh_password': None, 'ssh_public_key_path': None}
    if any(val is None for key, val in ssh_data.items()):
        for key in ssh_data:
            ssh_data[key] = click.prompt('Please enter value for (' + key + ')', default=None, type=str)
        with open(project_root + '/test/test_params.json', 'w') as params_file:
            json.dump(ssh_data, params_file)
    with warnings.catch_warnings(record=True):
        unittest.main()
