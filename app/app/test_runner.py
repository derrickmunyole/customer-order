import os
from django.test.runner import DiscoverRunner
from coverage import Coverage


class CoverageRunner(DiscoverRunner):
    def __init__(self, *args, **kwargs):

        coverage_dir = '/app/cov'
        os.makedirs(coverage_dir, exist_ok=True)

        self.coverage = Coverage(
            data_file=os.path.join(coverage_dir, '.coverage'),
            source=[
                'core',
                'customers',
                'orders',
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

        super().__init__(*args, **kwargs)

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        self.coverage.start()
        results = super(CoverageRunner, self).run_tests(
            test_labels=test_labels,
            extra_tests=extra_tests,
            **kwargs
        )
        self.coverage.stop()
        self.coverage.save()
        self.coverage.report()
        self.coverage.xml_report(outfile='./cov/.coverage.xml')

        return results
