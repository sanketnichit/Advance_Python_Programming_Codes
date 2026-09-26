# Assignment 6
# 0/1 Knapsack using Memoization and Tabulation

def knapsack_memo(weights, values, n, capacity, memo):

    # Base condition
    if n == 0 or capacity == 0:
        return 0

    # Check if already calculated
    if memo[n][capacity] != -1:
        return memo[n][capacity]

    # If current item is too heavy
    if weights[n - 1] > capacity:
        memo[n][capacity] = knapsack_memo(
            weights,
            values,
            n - 1,
            capacity,
            memo
        )

    else:
        # Include current item
        include = values[n - 1] + knapsack_memo(
            weights,
            values,
            n - 1,
            capacity - weights[n - 1],
            memo
        )

        # Exclude current item
        exclude = knapsack_memo(
            weights,
            values,
            n - 1,
            capacity,
            memo
        )

        memo[n][capacity] = max(include, exclude)

    return memo[n][capacity]


def knapsack_tabulation(weights, values, capacity):

    n = len(weights)

    # Create DP table
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # Fill DP table
    for i in range(1, n + 1):

        for w in range(1, capacity + 1):

            if weights[i - 1] <= w:

                include = values[i - 1] + dp[i - 1][w - weights[i - 1]]
                exclude = dp[i - 1][w]

                dp[i][w] = max(include, exclude)

            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]


# Input
n = int(input("Enter number of items: "))

weights = []
values = []

for i in range(n):
    print("\nItem", i + 1)

    weight = int(input("Enter weight: "))
    value = int(input("Enter value: "))

    weights.append(weight)
    values.append(value)

capacity = int(input("\nEnter bag capacity: "))

# Top-Down Memoization
memo = [[-1] * (capacity + 1) for _ in range(n + 1)]

result_memo = knapsack_memo(
    weights,
    values,
    n,
    capacity,
    memo
)

# Bottom-Up Tabulation
result_tabulation = knapsack_tabulation(
    weights,
    values,
    capacity
)

# Output
print("\nMaximum value using Memoization:", result_memo)
print("Maximum value using Tabulation:", result_tabulation)