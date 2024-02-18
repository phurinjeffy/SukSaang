
import matplotlib.pyplot as plt
from models import *

day1 = Statistic(day=1, cost= 120, income=140, popular="vegPiz")
day2 = Statistic(day=2, cost= 10, income=200, popular="Latte")
day31 = Statistic(day=31, cost= 0, income=0, popular="Latte")
days = [day1, day2, day31]

sales = [[s.day,s.income-s.cost]for s in days]
# print(sales)
# sales = [[1, 30], [2, 40], [3, 100], [4, 40], [31, 20]]

# Extracting days and corresponding sales
days = [day for day, _ in sales]
sales_values = [value for _, value in sales]
# print(days)
# print(sales_values)

# Creating the bar chart
plt.bar(days, sales_values)

# Adding labels and title
plt.xlabel('Day')
plt.ylabel('Sales ($)')
plt.title('Product Sales per Day')

# Displaying the plot
plt.show()
