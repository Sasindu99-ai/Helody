from PyQt5.QtGui import QIcon

from Components.Common.Button import Button
from Util import Styles


class MiniButton(Button):

    def __init__(self,
                 icon: str | QIcon,
                 tooltip: str,
                 action: callable = None):
        super(MiniButton, self).__init__(icon=icon,
                                         tooltip=tooltip,
                                         size=Styles.miniButtonSize,
                                         style=Styles.miniButton,
                                         padding=(10, 0),
                                         action=action)
