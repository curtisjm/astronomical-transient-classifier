class Transient:
    def __init__(self, times, rates, rate_errors, name, ra_dec, label):
        self.times = times
        self.rates = rates
        self.rate_errors = rate_errors
        self.name = name
        self.ra_dec = ra_dec
        self.label = label
        # self.ra = ra
        # self.dec = dec
