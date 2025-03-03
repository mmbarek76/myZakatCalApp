import streamlit as st
from PIL import Image


st.title("Zakat Al_Mal Calculation")


image1= Image.open('./Zakat_Pct.webp')
st.image(image1,width=555)
image2= Image.open('./Zakat_verse.jpg')
st.sidebar.image(image2)
# Input Data:
st.write("### Input Data:")

col1, col2 = st.columns(2)

col1.write("Please, enter your total cash(Bank balance):")
cashAmt_input = col1.number_input("Total Cash",min_value=0)
col1.write("Please, enter your gross 401K:")
retirmentAmt_input = col1.number_input("Total 401K",min_value=0)
filing_status = col1.selectbox(
    "# Please choose your filing status",
    ("single", "married_jointly", "head_of_household"),
)
col1.write("Please, enter your total expenses:")
expensesAmt_input =  col1.number_input("Total Expenses",min_value=0)

# Calculate Net 401K(# Gross 401k - FedTax - State Tax - 10% penality)
#**********************************
#   Calculate Fed Tax
#**********************************
def calculate_federal_tax(income, filing_status):
    tax_brackets = {
        'single': [
            (0, 11600, 0.10),
            (11600, 47150, 0.12),
            (47150, 100525, 0.22),
            (100525, 191950, 0.24),
            (191950, 243725, 0.32),
            (243725, 609350, 0.35),
            (609350, float('inf'), 0.37)
        ],
        'married_jointly': [
            (0, 23200, 0.10),
            (23200, 94300, 0.12),
            (94300, 201050, 0.22),
            (201050, 383900, 0.24),
            (383900, 487450, 0.32),
            (487450, 731200, 0.35),
            (731200, float('inf'), 0.37)
        ],
        'head_of_household': [
            (0, 16550, 0.10),
            (16550, 63100, 0.12),
            (63100, 100500, 0.22),
            (100500, 191950, 0.24),
            (191950, 243700, 0.32),
            (243700, 609350, 0.35),
            (609350, float('inf'), 0.37)
        ]
    }

    # Select the appropriate tax bracket based on filing status
    brackets = tax_brackets.get(filing_status.lower())
    tax = 0
    remaining_income = income

    # Calculate tax based on the brackets
    for bracket in brackets:
        lower, upper, rate = bracket
        if remaining_income <= 0:
            break
        taxable_amount = min(remaining_income, upper - lower + 1) if upper != float('inf') else remaining_income
        tax += taxable_amount * rate
        remaining_income -= taxable_amount

    return tax

#**********************************
#   Calculate State Tax
#**********************************
def calculate_state_tax_married_jointly(income):
    # 2024 Tax Brackets (Married Filing Jointly)
    tax_brackets =[
            (0, 3000, 0.02),
            (3001 , 5000, 0.03),
            (5001, 17000, 0.05),
            (17001, float('inf'), 0.0575)]

    tax = 0
    remaining_income = income

    # Calculate tax based on the brackets
    for bracket in tax_brackets:
        lower, upper, rate = bracket
        if remaining_income <= 0:
            break
        taxable_amount = min(remaining_income, upper - lower + 1) if upper != float('inf') else remaining_income
        tax += taxable_amount * rate
        remaining_income -= taxable_amount

    return tax

#**********************************
#   Net 401K= Gross 401k - FedTax - State Tax - 10% penality
#**********************************
def fourOneKCalculation(retirmentAmt,filing_status):
    # calculate Federal tax using tax brackett
    fedtax = calculate_federal_tax(retirmentAmt,filing_status)
    # print(f"Federal tax for income ${total401K}: ${tax:.2f}")
    # calculate State tax
    stateTax= calculate_state_tax_married_jointly(retirmentAmt)
    # calculate penality 10%
    penality= retirmentAmt * 0.1
    #Net 401K
    net401K= retirmentAmt-fedtax-stateTax-penality
    
    return net401K



def calculateZakat(cashAmt_input,expensesAmt_input):
    fourOneK= fourOneKCalculation(retirmentAmt_input,filing_status)
    #calculate new wealth
    netWealth= (cashAmt_input + fourOneK)-expensesAmt_input
    #calculate zakat (2.5%)
    zakatAmt= netWealth*0.025

    return round(zakatAmt,2)

# Process
zakatAmt_Due=calculateZakat(cashAmt_input,expensesAmt_input)

# Output
#st.metric(label="Zakat Amount to be paid:", value=zakatAmt_tobepaid)
col1.success(f"Zakat Amount Due: {zakatAmt_Due}")