import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

my_year = 1987
my_month = 7
my_day = 17
my_hour = 13
my_minute = 30
my_second = 15

my_date_time = datetime(my_year,my_month,my_day,my_hour,my_minute,my_second)

print(my_date_time)
print(my_date_time.day)