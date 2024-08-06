class CO2:

	def __init__(self, c0, year0, emission):
		self.c0 = c0
		self.y0 = year0
		self.emission = emission

	def get_ppm(self, year):
		t = year - self.y0
		ppm = self.c0 * (0.99 ** t) + self.emission * t / 2.3
		return ppm


