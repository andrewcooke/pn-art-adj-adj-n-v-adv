from brigit import GitException
from os.path import exists
from os import unlink
from unittest import TestCase

from pnartadjadjnvadv.gitfile import GitFile


TMP = '/tmp/gf-test'


class TestGitFile(TestCase):

    def assert_file(self, count, lines):
        assert exists(TMP)
        n = 0
        with open(TMP, 'r') as input:
            for line in input:
                line = line.strip()
                assert not line or line.startswith('#') or line in lines, line
                n += 1
        assert count == n, n

    def test_no_git(self):
        if exists(TMP): unlink(TMP)
        gf = GitFile('/tmp/gf-test')
        try: gf.write(True, 1234, 'with space')
        except GitException: pass
        self.assert_file(13, ('1234 with space'))
        try: gf.write(False, 5678, 'word')
        except GitException: pass
        self.assert_file(13, ('1234 with space'))
        try: gf.write(True, 5678, 'word')
        except GitException: pass
        self.assert_file(14, ('1234 with space', '5678 word'))
