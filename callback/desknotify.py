# -*- coding: utf-8 -*-

# (c) 2017, Deunz
#
#
# this is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# this is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible import constants as C
from ansible.plugins.callback import CallbackBase

colors_codes = {
    'black': u'#000000', 'bright gray': u'#778899',
    'blue': u'#0000FF', 'white': u'#FFFFFF',
    'green': u'#00FF00', 'bright blue': u'#87CEFA',
    'cyan': u'#00FFFF', 'bright green': u'#7CFC00',
    'red': u'#FF0000', 'bright cyan': u'#E0FFFF',
    'purple': u'#800080', 'bright red': u'#E0FFFF',
    'yellow': u'#FFFF00', 'bright purple': u'#E0FFFF',
    'dark gray': u'#A9A9A9', 'bright yellow': u'#FFFF00',
    'magenta': u'#FF00FF', 'bright magenta': u'#9932CC',
    'normal': None,
}


def stringc(color, my_str):
    color_span = colors_codes[color]
    if color_span is not None:
        return u"<span color=\"%s\">%s</span>" % (color_span, my_str)
    else:
        return u"%s" % my_str


def colorize(lead, num, color):
    """ Print 'lead' = 'num' in 'color' """
    if num != 0:
        return stringc(color, u"%s=%-15s" % (lead, str(num)))
    else:
        return u"%s=%-4s" % (lead, str(num))


def hostcolor(host, stats, color=True):
    if stats['failures'] != 0 or stats['unreachable'] != 0:
        return u"%-37s" % stringc('red', host)
    elif stats['changed'] != 0:
        return u"%-37s" % stringc('yellow', host)
    else:
        return u"%-37s" % stringc('green', host)


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'dfinish'

    def __init__(self, display=None):
        super(CallbackModule, self).__init__(display)

    def send_to_desktop(self, title, message):
        import gi
        gi.require_version('Notify', '0.7')
        from gi.repository import Notify
        Notify.init(title)
        Notify.Notification.new(message).show()
        Notify.uninit()

    def v2_playbook_on_stats(self, stats):
        print("Enter one here")
        hosts = sorted(stats.processed.keys())
        resume_action = []
        for h in hosts:
            t = stats.summarize(h)
            resume_action.append(u"%-32s : %-16s %-16s %-16s %-16s" % (
                hostcolor(h, t),
                colorize(u'ok', t['ok'], C.COLOR_OK),
                colorize(u'changed', t['changed'], C.COLOR_CHANGED),
                colorize(u'unreachable', t['unreachable'], C.COLOR_UNREACHABLE),
                colorize(u'failed', t['failures'], C.COLOR_ERROR))
                )
        self.send_to_desktop("Ansible", "<b>Ansible</b>\n" + "\n".join(resume_action))
