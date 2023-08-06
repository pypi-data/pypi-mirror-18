from unittest import TestCase
from conductr_cli.sandbox_features import VisualizationFeature, LoggingFeature, MonitoringFeature, collect_features

try:
    from unittest.mock import call, patch, MagicMock  # 3.3 and beyond
except ImportError:
    from mock import call, patch, MagicMock


class TestFeatures(TestCase):
    def test_collect_features(self):
        self.assertEqual([VisualizationFeature],
                         [type(f) for f in collect_features([['visualization']])])

        self.assertEqual([LoggingFeature],
                         [type(f) for f in collect_features([['logging']])])

        # enable dependencies
        self.assertEqual([LoggingFeature, MonitoringFeature],
                         [type(f) for f in collect_features([['monitoring']])])

        # allow explicit listing of dependencies
        self.assertEqual([LoggingFeature, MonitoringFeature],
                         [type(f) for f in collect_features([['logging'], ['monitoring']])])

        # topological ordering for dependencies
        self.assertEqual([LoggingFeature, MonitoringFeature],
                         [type(f) for f in collect_features([['monitoring'], ['logging']])])

        # topological ordering and ignore duplicates
        self.assertEqual([LoggingFeature, MonitoringFeature, VisualizationFeature],
                         [type(f) for f in collect_features([['monitoring'], ['visualization'], ['logging'], ['monitoring']])])

    def test_feature_args(self):
        self.assertEqual([(LoggingFeature, []), (MonitoringFeature, ['2.1.0'])],
                         [(type(f), f.args) for f in collect_features([['monitoring', '2.1.0']])])

        self.assertEqual([(LoggingFeature, []), (MonitoringFeature, ['snapshot', '2.1.0-20161018-43bab24'])],
                         [(type(f), f.args) for f in collect_features([['monitoring', 'snapshot', '2.1.0-20161018-43bab24']])])


class TestMonitoringFeature(TestCase):
    def test_grafana_bundle(self):
        self.assertEqual('cinnamon-grafana', MonitoringFeature([]).grafana_bundle()['name'])
        self.assertEqual('cinnamon-grafana', MonitoringFeature([]).grafana_bundle()['bundle'])

        self.assertEqual('cinnamon-grafana', MonitoringFeature(['v2']).grafana_bundle()['name'])
        self.assertEqual('cinnamon-grafana:v2', MonitoringFeature(['v2']).grafana_bundle()['bundle'])
        self.assertEqual('cinnamon-grafana:v2.1', MonitoringFeature(['v2.1']).grafana_bundle()['bundle'])
        self.assertEqual('cinnamon-grafana:v2.1.0', MonitoringFeature(['2.1.0']).grafana_bundle()['bundle'])
        self.assertEqual('cinnamon-grafana:v2.1.0.RC2', MonitoringFeature(['2.1.0-RC2']).grafana_bundle()['bundle'])

        self.assertEqual('lightbend/commercial-monitoring/cinnamon-grafana:v2.1.0.20161018.43bab24',
                         MonitoringFeature(['snapshot', '2.1.0-20161018-43bab24']).grafana_bundle()['bundle'])

    def test_start(self):
        run_mock = MagicMock()

        with patch('conductr_cli.conduct_main.run', run_mock):
            MonitoringFeature([]).start()

        self.assertEqual(run_mock.call_args_list, [
            call(['load', 'cinnamon-grafana'], configure_logging=False),
            call(['run', 'cinnamon-grafana'], configure_logging=False)
        ])
