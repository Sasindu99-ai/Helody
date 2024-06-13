from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QStyle, QStyleOptionSlider


class Slider(QSlider):

    def mousePressEvent(self, event):
        super(Slider, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            val = self.pixelPosToRangeValue(event.pos())
            self.setValue(val)

    def mouseMoveEvent(self, event):
        super(Slider, self).mouseMoveEvent(event)
        if event.buttons() == Qt.LeftButton:
            val = self.pixelPosToRangeValue(event.pos())
            self.setValue(val)

    def pixelPosToRangeValue(self, pos):  # noqa
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        gr = self.style().subControlRect(QStyle.CC_Slider, opt,
                                         QStyle.SC_SliderGroove, self)
        sr = self.style().subControlRect(QStyle.CC_Slider, opt,
                                         QStyle.SC_SliderHandle, self)

        slider_min = 0
        slider_max = 0
        if self.orientation() == Qt.Horizontal:
            slider_length = sr.width()
            slider_min = gr.x()
            slider_max = gr.right() - slider_length + 1
        if self.orientation() == Qt.Vertical:
            slider_length = sr.height()
            slider_min = gr.y()
            slider_max = gr.bottom() - slider_length + 1
        pr = pos - sr.center() + sr.topLeft()
        p = pr.x() if self.orientation() == Qt.Horizontal else pr.y()
        return QStyle.sliderValueFromPosition(self.minimum(), self.maximum(),
                                              p - slider_min,
                                              slider_max - slider_min,
                                              opt.upsideDown)
