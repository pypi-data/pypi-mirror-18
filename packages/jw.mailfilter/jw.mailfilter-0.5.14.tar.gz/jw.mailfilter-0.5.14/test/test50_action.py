from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import email
import unittest

import mock as mock
from mailfilter.action import ForwardAction
from mailfilter.folder import Folder
from jw.util.configuration import FromString

CONFIG = r"""
global:
    time-out: 60
    smtp:
        host: mail.wezel.info
        username: j
        password: powerpot,Q1..
        ssl: on

actions:
    - &spam-report
        - report-pyzor
        - report-badips
        - forward-to jw28670@knujon.net
        - move-to "Old Spam"
        - stop
    - &spam-move
        - move-to Spam
        - stop

checks:
    - &all
        - {filter: rbl, org: bl.spamcop.net, action: *spam-report}

accounts:
    wezel.info:
        address: mail.wezel.info
        ssl: on
        username: j
        password: powerpot,Q1..
        folders:
            - [INBOX, *all]
        enabled: yes
"""

def xxspawn(*args, **kwargs):
    print('SPAWN!')
    return args[1](*args[2:], **kwargs)

class TestAction(unittest.TestCase):
    def setUp(self):
        self.config = FromString(CONFIG)
        Folder._startImap = mock.MagicMock(return_value=True)
        self.folderConfig = self.config('accounts', 'wezel.info')
        self.folderConfig.get('address')
        self.folder = Folder(
            'Account',
            self.folderConfig('folders'),
            self.folderConfig,
            self.config('global')
        )


    def test_forward(self):
        action = ForwardAction(mock.Mock(), ['joe@ding.org'], self.config('global'))
        msg = email.message_from_file(open('test/body/positive_exact.msg'))
        with mock.patch('gevent.spawn', new=xxspawn):
            action.run(1, self.folder, msg)
            print('FLOP!')

if __name__ == '__main__':
    unittest.main()
