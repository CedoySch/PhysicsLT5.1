import sys
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QLineEdit, QGridLayout, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar


class SpringOscillationSimulation(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Энергетические превращения при колебании груза на пружине')

        self.layout = QVBoxLayout()
        self.grid_layout = QGridLayout()

        self.mass_input = QLineEdit()
        self.grid_layout.addWidget(QLabel('Масса груза (кг):'), 0, 0)
        self.grid_layout.addWidget(self.mass_input, 0, 1)

        self.k_input = QLineEdit()
        self.grid_layout.addWidget(QLabel('Коэффициент жесткости пружины k (Н/м):'), 1, 0)
        self.grid_layout.addWidget(self.k_input, 1, 1)

        self.b_input = QLineEdit()
        self.grid_layout.addWidget(QLabel('Коэффициент сопротивления среды b (кг/с):'), 2, 0)
        self.grid_layout.addWidget(self.b_input, 2, 1)

        self.layout.addLayout(self.grid_layout)

        self.start_button = QPushButton('Запустить симуляцию')
        self.start_button.clicked.connect(self.start_simulation)
        self.layout.addWidget(self.start_button)

        self.canvas = FigureCanvas(plt.figure())
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

    def show_error(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle('Ошибка')
        msg_box.setText(message)
        msg_box.exec_()

    def start_simulation(self):
        try:
            m = float(self.mass_input.text())
            k = float(self.k_input.text())
            b = float(self.b_input.text())

            if m <= 0:
                raise ValueError("Масса должна быть положительным числом.")
            if k <= 0:
                raise ValueError("Коэффициент жесткости должен быть положительным числом.")
            if b < 0:
                raise ValueError("Коэффициент сопротивления не может быть отрицательным.")
        except ValueError as e:
            self.show_error(str(e))
            return

        x0 = 0.1  # Начальное смещение в метрах
        v0 = 0.0  # Начальная скорость в м/с

        t = np.linspace(0, 20, 1000)

        def oscillator(y, t, m, k, b):
            x, v = y
            dydt = [v, -b / m * v - k / m * x]
            return dydt

        y0 = [x0, v0]
        sol = odeint(oscillator, y0, t, args=(m, k, b))
        x = sol[:, 0]
        v = sol[:, 1]

        KE = 0.5 * m * v ** 2
        PE = 0.5 * k * x ** 2
        E_total = KE + PE

        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.plot(t, KE, label='Кинетическая энергия')
        ax.plot(t, PE, label='Потенциальная энергия')
        ax.plot(t, E_total, label='Полная механическая энергия', linestyle='--')
        ax.set_xlabel('Время (с)')
        ax.set_ylabel('Энергия (Дж)')
        ax.set_title('Энергетические превращения при колебании груза на пружине')
        ax.legend()
        ax.grid(True)
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    window = SpringOscillationSimulation()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
