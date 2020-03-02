# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    arrays=[]
    for d in degs:
        arrays.append(pylab.polyfit(x,y,d))
    return arrays

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    mu = pylab.mean(y)
    SSE = pylab.sum((y-estimated)**2)
    SSW = pylab.sum((y-mu)**2)
    
    return 1-(SSE/SSW)

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    #set up plots
    pylab.rcParams['lines.linewidth'] = 2
    pylab.rcParams['axes.titlesize'] = 20
    pylab.rcParams['axes.labelsize'] = 20
    pylab.rcParams['xtick.labelsize'] = 16
    pylab.rcParams['ytick.labelsize'] = 16
    pylab.rcParams['xtick.major.size'] = 7
    pylab.rcParams['ytick.major.size'] = 7
    pylab.rcParams['lines.markersize'] = 10
    pylab.rcParams['legend.numpoints'] = 1
    pylab.xticks(pylab.arange(min(x), max(x)+1, 8))
    # pylab.yticks(pylab.arange(round(min(y)), round(max(y)),2))
    pylab.xlabel('Years')
    pylab.ylabel('Average Temperature in C')
    
    for m in models:
        estYVals = pylab.polyval(m,x)
        r2 = r_squared(y,estYVals)
        std_error = se_over_slope(x,y,estYVals,m)
        pylab.plot(x,estYVals,label = 'Fit of degree '\
                   + str(len(m)-1)\
                       + ', R2 = '+str(round(r2,3)) + ', SE/S = '+str(round(std_error,3)))
    pylab.legend(loc = 'best')
    pylab.title("Temperatures in Celcius")
    
    pylab.scatter(x,y,c='b',label = 'Data')
    pylab.show()
    

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    temps = []
    cities_avg = []
    for yr in years:
        for c in multi_cities:
            temps.append(climate.get_yearly_temp(c, yr))
        cities_avg.append(pylab.mean(temps))
        temps = []
    return pylab.array(cities_avg)
        
def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    temp = []
    result = []
    
    for k in range (len(y)):
        # temp.append(y[k])
        for i in range(k,k+window_length):
            if i-window_length+1 >= 0:       
                temp.append(y[i-window_length+1])
        result.append(sum(temp)/len(temp))
        temp = []

    return pylab.array(result)
    
def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    return pylab.sqrt(pylab.sum((y-estimated)**2)/len(y))
    
def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    # temps = []
    # std_dev=[]
    
    # for yr in years:
    #     for c in multi_cities:
    #         temps.append(climate.get_yearly_temp(c, yr))
    #     std_dev.append(pylab.std(temps))
    #     temps=[]
    # city_temperatures = []
    # avg_temps_day = []
    # yearly_std_dev = []
    # # return pylab.array(std_dev)
    # for year in years:
    #     avg_temps_day = []
    #     for month in range(1, 13):
    #         for day in range(1, 32):
    #             city_temperatures=[]
    #             for city in multi_cities:
    #                 if day in climate.rawdata[city][year][month]:
    #                     city_temperatures.append(climate.get_daily_temp(city, month, day, year))
    #             avg_temps_day.append(pylab.mean(city_temperatures))
    #             # print(avg_temps_day)
    #     yearly_std_dev.append(pylab.std(avg_temps_day))
        
        
    # return pylab.array(yearly_std_dev)

    std_devs_list = []
    for year in years:
        annual_temp = []
        for city in multi_cities:
            annual_temp_city = climate.get_yearly_temp(city, year)
            annual_temp.append(annual_temp_city)
        avg_annual_temp = []
        for i in range(len(annual_temp_city)):
            daily_temp = 0
            for j in range(len(annual_temp)):
                daily_temp += annual_temp[j][i]
            avg_annual_temp.append(daily_temp/len(annual_temp))
        std_devs_list.append(pylab.std(avg_annual_temp))

    return pylab.array(std_devs_list)

    

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    pylab.rcParams['lines.linewidth'] = 2
    pylab.rcParams['axes.titlesize'] = 20
    pylab.rcParams['axes.labelsize'] = 20
    pylab.rcParams['xtick.labelsize'] = 16
    pylab.rcParams['ytick.labelsize'] = 16
    pylab.rcParams['xtick.major.size'] = 7
    pylab.rcParams['ytick.major.size'] = 7
    pylab.rcParams['lines.markersize'] = 10
    pylab.rcParams['legend.numpoints'] = 1
    pylab.xticks(pylab.arange(min(x), max(x)+1))
    pylab.xlabel('Years')
    pylab.ylabel('Average Temperature in C')
    
    for m in models:
        estYVals = pylab.polyval(m,x)
        rm_se = rmse(y,estYVals)
        pylab.plot(x,estYVals,label = 'Fit of degree '\
                   + str(len(m)-1)\
                       + ', RMSE = '+str(round(rm_se,3)))
    pylab.legend(loc = 'best')
    pylab.title("Temperatures in Celcius")
    
    pylab.scatter(x,y,c='b',label = 'Data')
    pylab.show()

if __name__ == '__main__':
    clim = Climate('data.csv')
    
    # # Part A.4
    # #To generate values for January 10th in New York within the training_interval
    # temperatures = []
    # xVal = []
    # for year in TRAINING_INTERVAL:
    #     xVal.append(year)
    #     temperatures.append(clim.get_daily_temp('NEW YORK',1,10,year))
    # temperatures,xVal = pylab.array(temperatures),pylab.array(xVal)
    # models = generate_models(xVal,temperatures,[1])
    # evaluate_models_on_training(xVal,temperatures,models)
    
    #To generate values for New York average yearly temp within the training_interval
    # temperatures = []
    # xVal = []
    # for year in TRAINING_INTERVAL:
    #     xVal.append(year)
    #     temperatures.append(pylab.mean(clim.get_yearly_temp('NEW YORK',year)))
    # temperatures,xVal = pylab.array(temperatures),pylab.array(xVal)
    # models = generate_models(xVal,temperatures,[1])
    # evaluate_models_on_training(xVal,temperatures,models)
    
    # # Part B
    # #To plot charts for multiple cities across training_interval    
    # avg_temp = gen_cities_avg(clim,CITIES,pylab.array(TRAINING_INTERVAL))
    # models = generate_models(pylab.array(TRAINING_INTERVAL),avg_temp,[1])
    # evaluate_models_on_training(pylab.array(TRAINING_INTERVAL),avg_temp,models)
    
    # Part C
    # mov_avg = moving_average(gen_cities_avg(clim,CITIES,pylab.array(TRAINING_INTERVAL)),5)
    # models = generate_models(pylab.array(TRAINING_INTERVAL),mov_avg,[1])
    # evaluate_models_on_training(pylab.array(TRAINING_INTERVAL),mov_avg,models)
    
    # Part D.2
    #Training data
    # mov_avg = moving_average(gen_cities_avg(clim,CITIES,pylab.array(TRAINING_INTERVAL)),5)
    # models = generate_models(pylab.array(TRAINING_INTERVAL),mov_avg,[1,2,20])
    # evaluate_models_on_training(pylab.array(TRAINING_INTERVAL),mov_avg,models)
    
    #Testing data
    # mov_avg_2 = moving_average(gen_cities_avg(clim,CITIES,pylab.array(TESTING_INTERVAL)),5)
    # evaluate_models_on_testing(pylab.array(TESTING_INTERVAL),mov_avg_2,models)
    
    # Part E
    std_devs= gen_std_devs(clim,CITIES,pylab.array(TRAINING_INTERVAL))
    mov_avg_3=moving_average(std_devs,5)
    models = generate_models(pylab.array(TRAINING_INTERVAL),mov_avg_3,[1])
    evaluate_models_on_training(pylab.array(TRAINING_INTERVAL),mov_avg_3,models)
#Write-up portion
########Part A
# ● What difference does choosing a specific day to plot the data for versus
# calculating the yearly average have on our graphs (i.e., in terms of the R​ 2
# values and the fit of the resulting curves)? Interpret the results.
# > The yearly average is the aggregate of each day of the year. The volume of data considered
# in the yearly average results in a smoother trend, with greater predictive power.
# The single day temperature data is subject to climate fluctuations, and isn't smoothed out by the other days.
    
# ● Why do you think these graphs are so noisy? Which one is more noisy?
# > The data is across a large x-interval, and temperature is inconsistent and fluctuates across
# subsequent years typically. The noisier graph is the daily temp for January 10 in New York.
# There seems to be little fit between all the points -- fluctuations are immense.
    
# ● How do these graphs support or contradict the claim that global warming is
# leading to an increase in temperature? The slope and the standard
# error-to-slope ratio could be helpful in thinking about this.
# > The slope tilts upwards, suggesting an upward trend. 
# However for the January 10 stats, the SE/S is greater, suggesting that
# the yearly average data's line of fit is more reliable and a better predictor of trend.
# Thus the trend is only best observed by taking a the yearly mean for a time interval.
    
########Part B
# ● How does this graph compare to the graphs from part A ​(i.e., in terms of
# the R​ 2 values, the fit of the resulting curves, and whether the graph
# supports/contradicts our claim about global warming)? Interpret the
# results.
# > The R2 value is 0.746, indicating that this model has significant predictive power (R2 > 0.5). 
# The claim about global warming is thoroughly substantiated, as the trend is clearly marked by
# a positive slope, therefore a positive correlation between the year and average national temperature
# In compoarison to the graphs from part A, the R2 is above 0.5 indicating a significant trend, and the SE/S
# indicates little drift from the predictive model, suggesting that the average national temperature conforms
# to the hypothesis that there is a relationship between time and increase in temperature C.
    
# ● Why do you think this is the case?
# > This model incorporates more data -- the yearly average of all cities in America, which smooths
# the inconsistencies and potential errors, resulting in a more reliable trend. 
    
# ● How would we expect the results to differ if we used 3 different cities?
# What about 100 different cities?
# > The results from a sample of 3 different cities would not generate a smooth enough regression line,
# neither will the trend be as demonstrably visible as a sample of 100 different cities, simply
# due to the volume of the data and it's effect on the fit of the regression line. The more data
# we incorporate into the model, the more reliable it's predictive power.
    
# ● How would the results have changed if all 21 cities were in the same region
# of the United States (for ex., New England)?
# > The results would be insufficient in explananing a national trend of climate trend.
# The predictive power of this data as it attempts to describe a national climte trend would be weak
# and insubstantial. 
    
########Part C
# ● How does this graph compare to the graphs from part A and B (​i.e., in
# terms of the R​ 2​ values, the fit of the resulting curves, and whether the
# graph supports/contradicts our claim about global warming)? Interpret the
# results.
# > The R2 value here is significantly higher, almost 1, implying a strong predictive trend.
# The SE/S is also much lower, implying that the points have little error or deviation from the trend.
# ● Why do you think this is the case?
# The moving average incorporates the avg_temps from 5 years prior into a single point,
# allowing the data to become more congruent to the regression line, and demonstrates the trend
# across the training interval with smoother data.

########Problem D
#Problem 2.1
# ● How do these models compare to each other?
# > The lower the fit of degree, the lower the R2. This means that the higher the degree of
# of polynomial used to predict the results, the lower the variance from the prediction model.
# ● Which one has the best R 2 ? Why?
# The fit of degree 20 model has the best R2, as the lower the drift of the data points from the model,
# the higher the R2. 
# ● Which model best fits the data? Why?
# It appears the degree 20 model fits the data, as it conforms best with the fluctuations of the temperature
# points throughout the training interval, whereas the other models do not. 
    
#Problem 2.2
# ● How did the different models perform? How did their RMSEs compare?
# > Fit of degree 1 had the lowest RMSE, while fit of degree 20 had the highest. This indicates that 
# the degree 1 polynomial model had the best predictive power.
# ● Which model performed the best? Which model performed the worst? Are
# they the same as those in part D.2.I? Why?
# > The degree 20 model performed the worst, which is in opposition to how well it predicted the results
# of the training interval data.
# ● If we had generated the models using the A.4.II data (i.e. average annual
# temperature of New York City) instead of the 5-year moving average over
# 22 cities, how would the prediction results 2010-2015 have changed?
# > There may be a greater RMSE, as the spread on New York City avg temps across the training interval
# showed significant incomformity with the degree 1 trend line. 
    
########Problem E
# ● Does the result match our claim (i.e., temperature variation is getting
# larger over these years)?
# > Temperature variation appears to be decreasing over the years.
# ● Can you think of ways to improve our analysis?
# > As we are looking for extreme data, we should compare the variance of a single day
# to the average yearly temperature.