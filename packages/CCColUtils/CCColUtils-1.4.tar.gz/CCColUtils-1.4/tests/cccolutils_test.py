# Copyright 2016 Patrick Uiterwijk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import tempfile
import shutil
import sys
import os
import unittest

import cccolutils

class TestCCColUtils(unittest.TestCase):
    def setUp(self):
        self.testdir = tempfile.mkdtemp('cccolutils_krb')
        os.environ['KRB5CCNAME'] = 'DIR:%s' % self.testdir

        if sys.version_info[0] == 2:
            # krbV is used to hack the principals together
            import krbV

            ctx = krbV.Context()
            princ = krbV.Principal(name='myuser@EXAMPLE.COM', context=ctx)
            ccache = krbV.CCache(primary_principal=princ, context=ctx)

    def tearDown(self):
        shutil.rmtree(self.testdir)

    def test_get_user_from_realm(self):
        if sys.version_info[0] != 2:
            return
        self.assertEqual(cccolutils.get_user_for_realm('EXAMPLE.COM'), 'myuser')

    def test_get_user_from_realm_unknown_realm(self):
        self.assertEqual(cccolutils.get_user_for_realm('C.EXAMPLE'), None)

    def test_has_creds(self):
        self.assertFalse(cccolutils.has_creds())
