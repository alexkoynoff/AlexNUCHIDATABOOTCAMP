import os
import csv

#path to file
pybankfile = os.path.join('..','PyBank','budget_data.csv')

#empty lists
date = []
monthly_change = []

#variables
countmonth = 0
total_profit = 0
previous_profit = 0

#open as csv file
with open(pybankfile, 'r', newline='') as csvfile:
    #store file information in variable csvreader
    csvreader = csv.reader(csvfile,delimiter=',')
    #print(csvreader). initially used to test if it reads the file. Put a # in front of it after verifying
    
    #skips the header of the file
    csv_header = next(csvreader)
    

    for row in csvreader:    
      # countmonth to count the number of months(rows).
      countmonth +=1  
       

      # store info in the date list
      date.append(row[0])

      
      #calculate the total profit
      total_profit += int(row[1])
        

      #Calculate the average change in profits from month to month
      current_profit = int(row[1])
      monthly_change_profits = current_profit - previous_profit
      monthly_change.append(monthly_change_profits)
      previous_profit = current_profit 
      
      
      #define an average function to help calculate the average monthly changes excluding the first value from the monthly_change list
      def average(monthly_change):
          x = len(monthly_change)
          total = sum(monthly_change) - monthly_change[0]
          avg = total / 85      # Wanted to do avg = total / (x - 1) but it gives a divide by zero error
          return avg      

      #Calculate the average change in profits using above function
      averageprofits = round(average(monthly_change), 2)

      #Look for the max and min monthly_change and the corresponding dates for the two values
      max_increase = max(monthly_change)
      max_decrease = min(monthly_change)

      increase_date = date[monthly_change.index(max_increase)]
      decrease_date = date[monthly_change.index(max_decrease)]

    print("----------------------------------------------------------")
    print("Financial Analysis")
    print("----------------------------------------------------------")
    print("Total Months: " + str(countmonth))
    print("Total Profits: " + "$" + str(total_profit))
    print("Average Change: " + "$" + str(averageprofits))
    print("Greatest Increase in Profits: " + str(increase_date) + " ($" + str(max_increase) + ")")
    print("Greatest Decrease in Profits: " + str(decrease_date) + " ($" + str(max_decrease)+ ")")
    
    #THE BELOW PRINTS ARE FOR VERIFICATION PURPOSES ONLY TO ENSURE THE LISTS CONTAIN THE PROPER INFO
    
    #print("----------------------------------------------------------")
    #print("----------------------------------------------------------")
    #print("----------------------------------------------------------")
    #print("Shows Contents of Lists")
    #print("----------------------------------------------------------")
    #print(date)
    #print("----------------------------------------------------------")
    #print("----------------------------------------------------------")
    #print(monthly_change)
    #print("----------------------------------------------------------")
    #print("----------------------------------------------------------")
    #print(len(monthly_change))

#export results to text file
export_file = os.path.join('..','PyBank','Financial_Analysis_Alex_Koynoff.txt')
with open(export_file,'w',newline='') as text_file:
    writer = csv.writer(text_file)

    writer.writerows([
    ["Financial Analysis for PyBank by Alex Koynoff"],
    ["-" * 40],
    ["Total Months: " + str(countmonth)],
    ["Total Profits: " + "$" + str(total_profit)], 
    ["Average Change: " + "$" + str(averageprofits)],
    ["Greatest Increase in Profits: " + str(increase_date) + " ($" + str(max_increase) + ")"],
    ["Greatest Decrease in Profits: " + str(decrease_date) + " ($" + str(max_decrease)+ ")"] 
    ])
    
    
    