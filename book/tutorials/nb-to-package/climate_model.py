import numpy as np
import matplotlib.pyplot as plt
from co2_emissions import CO2

class VSCM:

	def __init__(self, start_year, emd_year, co2_ppm, sensitivity, c0, t0):
		self.y_start = start_year
		self.y_end = emd_year
		self.s = sensitivity
		self._co2_ppm = co2_ppm
		self.time = [start_year]
		self.temp = [t0]
		self.co2 = [c0]


	def run(self):
		i = 0
		while i + self.y_start <= self.y_end:
			year = self.y_start + i
			t0 = self.temp[-1]
			c0 = self.co2[-1]
			c = self._co2_ppm.get_ppm(year)
			t = t0 + self.s * np.log2(c / c0)

			self.time.append(year)
			self.co2.append(c)
			self.temp.append(t)

			i += 1

	def plot(self):
		fig, ax = plt.subplots(layout='constrained')

		col = 'tab:red'
		ax.plot(self.time, self.temp, color=col)
		ax.set_xlabel('Year')
		ax.set_ylabel(r'$T\ (^oC)$', color=col)

		ax2 = ax.twinx()
		col = 'tab:blue'
		ax2.plot(self.time, self.co2, color=col)
		ax2.set_ylabel('$C0_2 (ppm)$', color=col)

		plt.show()



if __name__ == '__main__':
	start_year = 2015
	end_year = 2115
	c0 = 400
	co2_ppm = CO2(c0, start_year, 10)
	t0 = 14.65

	my_model = VSCM(start_year, end_year, co2_ppm, 3, c0, 14.65)
	my_model.run()
	my_model.plot()
