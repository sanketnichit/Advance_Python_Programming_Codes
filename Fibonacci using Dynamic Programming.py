# Assignment 4
# Fibonacci using Memoization and Tabulation

def fibonacci_memo(n, memo):
    if n <= 1:
        return n

    if n in memo:
        return memo[n]

    memo[n] = (
        fibonacci_memo(n - 1, memo)
        + fibonacci_memo(n - 2, memo)
    )

    return memo[n]


def fibonacci_tabulation(n):
    if n <= 1:
        return n

    dp = [0] * (n + 1)

    dp[0] = 0
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


# Input
n = int(input("Enter the value of n: "))

# Top-Down
memo = {}
result_memo = fibonacci_memo(n, memo)

# Bottom-Up
result_tabulation = fibonacci_tabulation(n)

# Output
print("\nUsing Memoization:", result_memo)
print("Using Tabulation:", result_tabulation)