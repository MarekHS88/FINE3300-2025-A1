# Assignment 1: Mortgage Calculator
# FINE 3300: Project 1 
# Marek Satov

# create class for mortgage payments 
class MortgagePayment:
    def __init__(self, rate, years): # store rate and years
        self.rate = rate / 100 # convert percentage to decimal
        self.years = years # store years

    def payments(self, principal):
        # Convert quoted semi-annual nominal rate to an (EAR)
        ear = (1 + (self.rate / 2))**2 - 1

        #Get the rate for each schedule from the EAR
        r_mo  = (1 + ear)**(1/12) - 1          # monthly
        r_sm  = (1 + ear)**(1/24) - 1          # semi-monthly (24/yr)
        r_bw  = (1 + ear)**(1/26) - 1          # bi-weekly (26/yr)
        r_wk  = (1 + ear)**(1/52) - 1          # weekly (52/yr)

        #Number of payments for each schedule
        n_mo = self.years * 12          # monthly
        n_sm = self.years * 24          # semi-monthly
        n_bw = self.years * 26          # bi-weekly
        n_wk = self.years * 52          # weekly

        # Calculate the payment for each schedule using PV formula
        # Payment = P * r / (1 - (1+r)^-n)
        def pay(P, r, n): return P * r / (1 - (1 + r)**(-n))

        monthly = pay(principal, r_mo, n_mo)    
        semi_monthly = pay(principal, r_sm, n_sm)
        bi_weekly = pay(principal, r_bw, n_bw)
        weekly = pay(principal, r_wk, n_wk)

        #Rapid payments are defined off the monthly
        rapid_bi_weekly = monthly / 2
        rapid_weekly = monthly / 4

        return (monthly, semi_monthly, bi_weekly, weekly, rapid_bi_weekly, rapid_weekly)

# Running the program 
# Making a prompt for the user to input the values
p = float(input("Enter mortgage principal: ")) #principal
r = float(input("Enter interest rate (%): ")) #rate
y = int(input("Enter amortization period (years): ")) #years

# Create an object of the class
mortgage = MortgagePayment(r, y)

# Get the results
results = mortgage.payments(p)

labels = [
    "Monthly Payment",
    "Semi-Monthly Payment",
    "Bi-Weekly Payment",
    "Weekly Payment",
    "Rapid Bi-Weekly Payment",
    "Rapid Weekly Payment"
] # Labels for each payment type

# That line loops through each payment type and its value together, printing them neatly with two decimal places.
for label, value in zip(labels, results):
        print(f"{label}: ${value:.2f}")

        # For this last line I used Zip to pair the two lists together, labels and resluts comibes them, then I made a loop so it takes one item to label then one to value)
        # The f string is used to format the output, :.2f means 2 decimal places for float values
