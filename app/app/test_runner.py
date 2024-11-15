import os
from django.test.runner import DiscoverRunner
from coverage import Coverage


class CoverageRunner(DiscoverRunner):
    def __init__(self, *args, **kwargs):
        self.coverage = Coverage(
            data_file=os.path.join('/app/cov/.coverage'),
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
        self.coverage.xml_report(outfile='/app/cov/.coverage.xml')
        
        return results
