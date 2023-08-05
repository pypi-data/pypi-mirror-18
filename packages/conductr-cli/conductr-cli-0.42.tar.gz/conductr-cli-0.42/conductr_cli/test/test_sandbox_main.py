from unittest import TestCase
from conductr_cli import sandbox_main
from conductr_cli.sandbox_common import LATEST_CONDUCTR_VERSION, CONDUCTR_DEV_IMAGE


class TestSandbox(TestCase):

    parser = sandbox_main.build_parser()

    def test_parser_run_default_args(self):
        args = self.parser.parse_args('run {}'.format(LATEST_CONDUCTR_VERSION).split())
        self.assertEqual(args.func.__name__, 'run')
        self.assertEqual(args.image_version, LATEST_CONDUCTR_VERSION)
        self.assertEqual(args.conductr_roles, [])
        self.assertEqual(args.envs, [])
        self.assertEqual(args.image, CONDUCTR_DEV_IMAGE)
        self.assertEqual(args.log_level, 'info')
        self.assertEqual(args.nr_of_containers, 1)
        self.assertEqual(args.ports, [])
        self.assertEqual(args.features, [])
        self.assertEqual(args.local_connection, True)
        self.assertEqual(args.resolve_ip, True)

    def test_parser_run_custom_args(self):
        args = self.parser.parse_args('run 1.1.0 '
                                      '--conductr-role role1 role2 -r role3 '
                                      '--env env1 -e env2 '
                                      '--image my-image '
                                      '--log-level debug '
                                      '--nr-of-containers 5 '
                                      '--port 1000 -p 1001 '
                                      '--bundle-http-port 7111 '
                                      '--feature visualization -f logging -f monitoring 2.1.0'.split())
        self.assertEqual(args.func.__name__, 'run')
        self.assertEqual(args.image_version, '1.1.0')
        self.assertEqual(args.conductr_roles, [['role1', 'role2'], ['role3']])
        self.assertEqual(args.envs, ['env1', 'env2'])
        self.assertEqual(args.image, 'my-image')
        self.assertEqual(args.log_level, 'debug')
        self.assertEqual(args.nr_of_containers, 5)
        self.assertEqual(args.ports, [1000, 1001])
        self.assertEqual(args.features, [['visualization'], ['logging'], ['monitoring', '2.1.0']])
        self.assertEqual(args.local_connection, True)
        self.assertEqual(args.resolve_ip, True)
        self.assertEqual(args.bundle_http_port, 7111)

    def test_parser_stop(self):
        args = self.parser.parse_args('stop'.split())
        self.assertEqual(args.func.__name__, 'stop')
        self.assertEqual(args.local_connection, True)
        self.assertEqual(args.resolve_ip, True)

    def test_parser_debug(self):
        args = self.parser.parse_args('debug'.split())
        self.assertEqual(args.func, 'debug')
        self.assertEqual(args.resolve_ip, False)

    def test_parser_init(self):
        args = self.parser.parse_args('init'.split())
        self.assertEqual(args.func.__name__, 'init')
        self.assertEqual(args.resolve_ip, False)
