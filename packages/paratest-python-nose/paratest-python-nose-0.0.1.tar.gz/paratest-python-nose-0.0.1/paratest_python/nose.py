import os
import re
import subprocess


def find(path, test_pattern, file_pattern, output_path):
    output = subprocess.check_output('nosetests --collect-only -v')
    # 'output' contains lines like: test (suite) ... ok

    suites = set()

    for line in output.splitlines():
        if not line.strip():
            break
        m = re.match('.*\((?P<suite>.*)\).*', a)
        if not m:
            continue
        suites.add(m.group('suite'))

    for suite in suites:
        output = os.path.join(output_path, suite + '.xml')
        command = 'nosetests %s --with-xunit --xunit-file=%s' % (suite, output)
        yield suite, command
