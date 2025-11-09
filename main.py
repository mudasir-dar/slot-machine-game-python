"""
🎰 SLOT MACHINE GAME 🎰
A simple console-based slot machine built with Python.

Author: Mudasir Ahmad Dar
Description:
This program allows users to deposit money, place bets on 1–3 lines, 
and spin a virtual slot machine. Winnings are calculated based on matching 
symbols across selected lines.
"""



import secrets
import time


MAX_LINES = 3
MIN_BET = 1
MAX_BET = 100

ROWS = 3
COLS = 3

symbol_count = {
    "A" : 3,
    "B" : 4,
    "C" : 6,
    "D" : 8
}   

symbol_value = {
    "A" : 10,
    "B" : 8,
    "C" : 6,
    "D" : 4
} 

# ----------------- FUNCTIONS ----------------- #
def check_winnings(columns, lines, bet, values):
    """
    Checks which lines have matching symbols and calculates winnings.
    """
    winnings = 0
    winning_lines  = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet 
            winning_lines.append(line + 1)
            
    return winnings, winning_lines               

def get_slot_machine_spin(rows, cols, symbols):
    """
    Generates a cryptographically secure random spin result.
    """
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)
            
    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            # Secure random symbol selection
            value = secrets.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
        
    return columns


def print_slot_machine(columns):
    """
    Displays the slot machine result in a grid format.
    """
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")  
          
            time.sleep(0.3)             
            
        print()    
            

def deposit():
    """
    Secure deposit input validation to prevent invalid or negative entries.
    """
    while True:
        amount = input("Enter the amount you want to deposit: $ ").strip()
        if not amount.isdigit():
            print("❌ Please enter a valid positive number (digits only).")
            continue
        
        amount = int(amount)
        if amount <= 0:
            print("⚠️ Deposit amount must be greater than zero.")
        else:
            return amount


def number_of_lines():
    while True:
        lines = input("Enter the lines you want to bet on (1 - " + str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Enter a Valid number of Lines")
        else:
            print("Please Enter a number")
            
    return lines 


def get_bet():
    """
    Securely prompts the user for a valid bet amount with strict validation.
    Prevents negative numbers, symbols, or empty input.
    """
    while True:
        amount = input(f"Enter your bet per line (${MIN_BET}-${MAX_BET}): ").strip()
        
        # Check if input is purely digits
        if not amount.isdigit():
            print("❌ Invalid input. Please enter a positive whole number.")
            continue
        
        amount = int(amount)
        
        # Range validation
        if amount < MIN_BET:
            print(f"⚠️ Minimum bet per line is ${MIN_BET}.")
        elif amount > MAX_BET:
            print(f"⚠️ Maximum bet per line is ${MAX_BET}.")
        else:
            return amount

 
def spin(balance):
    #Handles a single spin round and returns balance change.
    
    lines = number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines
        
        if total_bet > balance:
            print(f"⚠️ Insufficient balance. Your balance is: ${balance}")
        else:
            break    
            
    print(f"\n🎲 You are betting ${bet} on {lines} lines. Total Bet = ${total_bet} ")
        
    # Confirm bet if it's more than half of balance (extra safety)
    if total_bet > balance / 2:
        confirm = input(f"⚠️ You're betting more than half your balance (${balance}). Continue? (y/n): ").lower()
        if confirm != "y":
            print("Bet canceled. Adjust your bet amount.")
            return 0

   
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    
    winnings, winning_lines = check_winnings(slots, lines, bet,  symbol_value)
    print(f"\n💰 You won ${winnings}.")
    if winnings > 0:
        print(f"🎉 Winning lines: {', '.join(map(str, winning_lines))}")
    else:
        print("Better luck next time!") 
        
    return winnings - total_bet  

def main():
    
    balance = deposit()
    
    while True:
        print(f"Current balance is ${balance}")
          
          #Check for empty balance
        if balance <= 0:
            print("❌ You have no balance left.")
            choice = input("Do you want to deposit more? (y/n): ").lower()
            if choice == "y":
                balance += deposit()
                continue
            else:
                print("Thanks for playing! 🎰")
                break
            
        answer = input("Press Enter to play (or 'q' to quit): ").lower()
        if answer == "q":
            break
        balance += spin(balance)
    
    print(f"\nThanks for playing! You left with ${balance} 💵")
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nThanks for playing! Goodbye 👋")
