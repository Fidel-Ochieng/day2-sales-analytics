Day 2 sales Analysis Without Pandas
Overview 
This project analyses data from five stores. we are required to calculate total revenue, identify the best-performing products, and find high-value transactions that need follow-up.
The analysis uses Python's standard library without pandas.Pandas is used only at the end to verify the results. 

How to run 
1. install python
2. pip install -r requirements.txt
3. python sales_analysis.py
4. save repotr to output/sales_report.txt



Approach 
1. Read data with data used csv.DictReader to load 50 sales record from csv file.
2. Clean data used convert_rows to clean quantity and unit price values.
3. Calculate revenue used total revenue to calculate total sales revenue.
4. Group sales. Used dictionaries and revenue_by to calculate revenue by products 
5. Rank Products used sorted()and top_n to identify three highest-earning products 
6. Filtered transactions using list comprehension to identify the sales worth KES 50,000 and above 
7. Calculate Statistics: calculated mean, median , minimum and maximum calculations manually. 
8. Verified results using pandas to check main calculations.

Data Cleaning 
I skipped records with missing or negative values  rather than guessing them it also skips values that aren't numbers.
 Out of 50 records, 46 were successfully proccessed leaving a side 4 which were skipped to hinder unreliable data from affecting results.



Results for September 2026
Total Revenue: KES 1310812.00
Top-Performing product:HP 15Laptop @KES 389994.00
Second:Hisense 43in smart TV, @KES 272993.00.
High-valued transactions: 5 sales worth KES 50,000 or more.
Verification:All checked values matched the pandas results.

Key Lesson Learned
I learned the importance of testing results independently and ensuring that both methods apply the same data-cleaning rules.

Assumption
Revenue is quantity times unit price, and that "high-value" means KES 50,000 or more