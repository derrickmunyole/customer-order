from django.test.runner import DiscoverRunner
from coverage import Coverage


class CoverageRunner(DiscoverRunner):
    def __init__(self, *args, **kwargs):
        self.coverage = Coverage(
            data_file='/tmp/.coverage',
            source=[
                'core',
                'customers',
                'orders',
                'orders'
                'users',
                'authentication'
                ],
            omit=[
                '*/tests/*',
                '*/migrations/*',
                '*/admin.py',
                '*/apps.py',
                'manage.py'
            ]

        )

        super.__init__(*args, **kwargs)

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        self.coverage.start()
        results = super.run_tests(
            test_labels,
            extra_tests,
            **kwargs
        )
        self.coverage.stop()
        self.coverage.html_report('coverage')

        return results
