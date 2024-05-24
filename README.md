# Scrooge Budget
Fundamentals of Programming &amp; Computer Science Capstone project for Turing College

Instructions
-------------
- Run application: python -m scr.main

- Exit program at any time by pressing 'Ctrl + D' (Unix terminal)  or 'Ctrl + Z Enter' (Windows terminal)

- Go back from any submenu up one level by entering 'back'

- In any menu mode/category can be chosen by entering corresponding number, first letter of the mode

## Menu
### **1. Balance & Savings:** 
    Requirement: Choose profile first

* ### Income/Expense
    - Enter 'income' or 'expense to add or remove monetary value to/from the account
    - Enter amount in digits to finalise the operation

* ### Current Balance
    - Outstanding account balance is shown

* ### Savings
    * Deposit/withdraw
        - Enter 'deposit' or withdraw to add or remove monetary value to/from savings account
        - The savings amount can interact only with existing balance

    * Current savings balance
        - Shows current savings balance

    * Savings goal
        - Enter digits on how many percents of current month income you would like to save this month
        - Amount will be shown for informative reasons, it will not be added automatically

    * Forecast

            Choose 'real' to work with saved values or custom to enter new values 
        * Date when wanted savings amount could be reached
            * Enter the wanted amount in savings
            * Message with amount & date will be printed out  
        * Amount of savings on specific date
            * Enter the date in format YYYY-MM
            * The amount of savings on the provided date will be printed out
---   		
### **2. Statistics**
      Requirement: Choose profile first
- Income/expense stats
    - Balance, income & expense amounts will be printed in a table on specific months
- Savings stats
    - Savings amount on specific months will be printed out
---
### **3. Profile**
- Enter the existing username or create new one
---
###  **4. Options**
- Change message/error separator
    - Default separator is '-'
    - Enter any 1 character to set a new separator 
- Change messages to uppercase, lowercase or titlecase
    - Default case is uppercase
    - Enter lowercase, titlecase or uppercase to set messages's case
---
### **5. Exit**
- Exist out of program
      
   
