# Very Simpl Climate Model
##########################

import numpy as np
import matplotlib.pyplot as plt
from co2_emissions import Constant_CO2, SSPEmissions

class VSCM:

	def __init__(self, start_year, t0, c0, sensitivity, co2_ppm):
		self.y0 = start_year
		self.s = sensitivity
		self._co2_ppm = co2_ppm
		self.time = [start_year]
		self.temp = [t0]
		self.co2 = [c0]


	def run(self, end_year):
		i = 0
		while i + self.time[-1] <= end_year:
			year = self.y0 + i
			t0 = self.temp[-1]
			c0 = self.co2[-1]
			c = self._co2_ppm.get_CO2_ppm(year)
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
	c0 = 400
	t0 = 14.65

	# constant emission scheme
	co2_ppm = Constant_CO2(c0, start_year, 10)

	# ssp scenario
	co2_ppm = SSPEmissions(126)


	my_model = VSCM(start_year, t0,  c0, 3, co2_ppm)
	my_model.run(2100)
	my_model.plot()
