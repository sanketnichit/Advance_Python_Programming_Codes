    # ------------------------------------------------------------
# Practical: Efficient Fibonacci Number using Dynamic Programming
# ------------------------------------------------------------

# -------------------- Memoization --------------------

def fibonacci_memo(n, cache):
    if n < 2:
        return n

    if n in cache:
        return cache[n]

    cache[n] = fibonacci_memo(n - 1, cache) + fibonacci_memo(n - 2, cache)
    return cache[n]


# -------------------- Tabulation --------------------

def fibonacci_tabulation(n):
    if n < 2:
        return n

    previous = 0
    current = 1

    for position in range(2, n + 1):
        next_value = previous + current
        previous = current
        current = next_value

    return current


# -------------------- Display Sequence --------------------

def display_sequence(n):
    print("\nFibonacci Sequence:")

    for i in range(n + 1):
        print(fibonacci_tabulation(i), end=" ")

    print()


# -------------------- Comparison --------------------

def compare_methods(n):
    memo_result = fibonacci_memo(n, {})
    table_result = fibonacci_tabulation(n)

    print("\n========== RESULTS ==========")
    print("Input n                :", n)
    print("Memoization Result     :", memo_result)
    print("Tabulation Result      :", table_result)

    if memo_result == table_result:
        print("Status                 : Both methods give the same result.")
    else:
        print("Status                 : Results do not match.")


# -------------------- Main Program --------------------

print("==============================================")
print("      EFFICIENT FIBONACCI NUMBER")
print("        USING DYNAMIC PROGRAMMING")
print("==============================================")

while True:

    try:
        number = int(input("\nEnter the value of n: "))

        if number < 0:
            print("Please enter a non-negative integer.")
            continue

        break

    except ValueError:
        print("Invalid input! Enter an integer.")


# Calculate using Memoization
memoization_answer = fibonacci_memo(number, {})

# Calculate using Tabulation
tabulation_answer = fibonacci_tabulation(number)

print("\n----------------------------------------------")
print("Memoization (Top-Down) :", memoization_answer)
print("Tabulation (Bottom-Up) :", tabulation_answer)
print("----------------------------------------------")

# Verify both methods
compare_methods(number)

# Display sequence for reasonable input
if number <= 30:
    display_sequence(number)

print("\n==============================================")
print("Time Complexity:")
print("Memoization : O(n)")
print("Tabulation  : O(n)")
print()
print("Space Complexity:")
print("Memoization : O(n)")
print("Tabulation  : O(1)")
print("==============================================")