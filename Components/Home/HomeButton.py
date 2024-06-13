from PyQt5.QtGui import QIcon

from Components.Common.Button import Button
from Util import Styles


class HomeButton(Button):

    def __init__(self,
                 icon: str | QIcon,
                 tooltip: str,
                 action: callable = None):
        super(HomeButton, self).__init__(icon=icon,
                                         tooltip=tooltip,
                                         size=Styles.defaultButtonSize,
                                         style=Styles.defaultButton,
                                         padding=(10, 10),
                                         action=action)
