from plan_maker import PlanMaker

def read(plan_tuples, conversion_rates=False, scenarios=True):

    if not isinstance(conversion_rates, bool):
        try:
            p = PlanMaker(plan_tuples, conversion_rates)
        except:
            print "Could not retrieve currency conversion rates." 
            p = False

    else:
		p = PlanMaker(plan_tuples)

    if p:
        if scenarios:
            return p.get_scenarios()
        else:
            return p
    else:
		print "Could not read the plan_tuples."
		return False

import fred
import requests
import pandas as pd

class Plan(object):
    def __init__(self):
        self.set_hour_rate()
        self.set_currenc_rates()

    def set_hour_rate(self, h=None):
        if h:
            self.hour = h
            print "Hour value of work (self.hour) was set to %s usd from FRED API. Retrieving currency rates.." % self.hour
            self.set_currenc_rates()
            print "Done."
        else:
            fred.key('0c9a5ec8dd8c63ab8cbec6514a8f5b37')
            last_observation = fred.observations(
                settings.FRED_SERIES)['observations'][-1]
            h = last_observation['value']
            try:
                self.hour = float(h)
                print "Hour value of work (self.hour) was set to %s usd from FRED API." % self.hour
            except:
                self.hour = 25.
                print "Failed to retrieve rates from FRED API. Assuming 1h = 25usd."

    def set_currenc_rates(self):
        currency_rates = requests.get('http://api.fixer.io/latest?base=USD').json()['rates']
        self.rates = pd.DataFrame( dict({'h': [self.hour], 'usd': 1.}, **{key.lower(): 1/currency_rates[key] for ix, key in enumerate(currency_rates)} ) )
        print "Currency values had been set from FIXER IO, check the .rates attribute.\nThe currency 'h' means the time of 1 hour labor, based on FRED API."

    def from_records(self, plan_dict):
        self.info = read([(step['input'], step['output']) for step in plan_dict], 
                       conversion_rates=self.rates,
                       scenarios=False)# * (rates['h'] / rates['gbp']).values[0]
        self.df = self.info.get_scenarios()
        return self.df

    def steps(self, plan_dict):
        return self.from_records(plan_dict)

    def plot(self, figsize=(10,4.5)):
        self.df['worst'].dropna().plot(marker='.', figsize=figsize)
        self.df['mean'].dropna().plot(marker='.', figsize=figsize)
        p = self.df['best'].dropna().plot(marker='.', figsize=figsize)
        p.set_ylabel('time (h, as value)')
        p.set_xlabel('time (h, elapsed)');
        p.grid(True)
