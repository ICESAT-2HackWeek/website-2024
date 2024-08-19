import pandas as pd

class BaseCO2:
	def __init__(self, scheme):
		self._scheme = str(scheme)

	def get_CO2_ppm(self, year):
		raise NotImplementedError

class Constant_CO2(BaseCO2):

	def __init__(self, c0, year0, emission_rate):
		super().__init__('constant')
		self.c0 = c0
		self.y0 = year0
		self.rate = emission_rate


	def get_CO2_ppm(self, year):
		n = year - self.y0
		k = 0.999
		a = self.rate*0.45/2.3
		ppm = k**n * (self.c0) + a*((1-k**n)/(1-k))

		return ppm


class SSPEmissions(BaseCO2):

	def __init__(self, scheme):
		super().__init__(scheme)
		self._years = None
		self._co2 = None
		self._read_ssp_csv()

	def __str__(self):
		return 'CO2 emission scheme: SSP{0}'.format(self._scheme)
	def _read_ssp_csv(self):
		df = pd.read_csv('SSP_CO2emissions.csv', skiprows=1)
		self._years = df['Year']
		self._co2 = df[self._scheme]

	def get_CO2_ppm(self, year):
		i = year - self._years[0]
		return self._co2[i]


if __name__ == '__main__':
	my_ssp = SSPEmissions(126)
	print(my_ssp)
	ppm = my_ssp.get_CO2_ppm(2033)
	print(ppm)


	const = Constant_CO2(409.36, 2020, 10)
	print(const)
	ppm = const.get_CO2_ppm(2025)
	print(ppm)