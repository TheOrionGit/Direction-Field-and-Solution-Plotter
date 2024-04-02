from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
import sys
import directfieldproj
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np
from scipy.integrate import odeint


class matplotlibwidget(QWidget):
    def __init__(self, parent=None):
        super(matplotlibwidget, self).__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axis = self.figure.add_subplot(111)
        self.layoutvertical = QVBoxLayout(self)
        self.layoutvertical.addWidget(self.canvas)


class MainWidget(QWidget, directfieldproj.Ui_Form):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.setupUi(self)
        self.init_widget()
        self.pushButton.clicked.connect(self.plot_widget)

    def init_widget(self):
        self.matplotlibwidget = matplotlibwidget()
        self.layoutvertical = QVBoxLayout(self.widget)
        self.layoutvertical.addWidget(self.matplotlibwidget)

    def plot_widget(self):
        self.matplotlibwidget.axis.clear()
        dxdt1 = self.lineEditdxdt.text()
        dydt1 = self.lineEditdydt.text()

        def pend(X, t):
            dxdt = eval(dxdt1.replace("y", "X[1]").replace("x", "X[0]")
                        .replace("sin", "np.sin").replace("cos", "np.cos").replace("tan", "np.tan"))
            dydt = eval(dydt1.replace("y", "X[1]").replace("x", "X[0]")
                        .replace("sin", "np.sin").replace("cos", "np.cos").replace("tan", "np.tan"))
            return [dxdt, dydt]

        tmin, tmax = float(self.lineEditTmin.text() or "-10"), float(self.lineEditTmax.text() or "10")
        t = np.linspace(tmin, tmax, 500)

        X10 = [int(self.lineEditYmin_2.text() or "0"), int(self.lineEditYmax_2.text() or "0")]
        X20 = [int(self.lineEditYmin_3.text() or "0"), int(self.lineEditYmax_3.text() or "0")]

        X1 = odeint(pend, X10, t)
        X2 = odeint(pend, X20, t)

        arrowDens = 1 / (float(self.ArrowDensBox.text()))
        nx, ny = arrowDens, arrowDens
        x = np.arange(int(self.lineEditXmin.text()), int(self.lineEditXmax.text()), nx)
        y = np.arange(int(self.lineEditYmin.text()), int(self.lineEditYmax.text()), ny)
        X, Y = np.meshgrid(x, y)
        dx = eval(dxdt1.replace("y", "Y").replace("x", "X")
                  .replace("sin", "np.sin").replace("cos", "np.cos").replace("tan", "np.tan"))
        dy = eval(dydt1.replace("y", "Y").replace("x", "X")
                  .replace("sin", "np.sin").replace("cos", "np.cos").replace("tan", "np.tan"))
        self.matplotlibwidget.axis.plot(X1[:, 0], X1[:, 1], color="black")
        self.matplotlibwidget.axis.plot(X2[:, 0], X2[:, 1], color="black")
        self.matplotlibwidget.axis.quiver(X, Y, dx, dy, color= self.ColorBox.currentText())
        self.matplotlibwidget.axis.set_xlim(int(self.lineEditXmin.text()) + 1, int(self.lineEditXmax.text()) - 1)
        self.matplotlibwidget.axis.set_ylim(int(self.lineEditYmin.text()) + 1, int(self.lineEditYmax.text()) - 1)
        self.matplotlibwidget.axis.set_title(self.lineEditTitle.text() or "")
        self.matplotlibwidget.axis.set_xlabel(self.lineEditXLabel.text() or "")
        self.matplotlibwidget.axis.set_ylabel(self.lineEditYLabel.text() or "")
        self.matplotlibwidget.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWidget()
    w.show()
    sys.exit(app.exec_())
