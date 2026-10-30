# Open the text file
file = open("sample.txt", "r")

lines = file.readlines()
file.close()

longest_line = ""
line_number = 0

# Find the longest line
for i, line in enumerate(lines, start=1):
    if len(line.strip()) > len(longest_line):
        longest_line = line.strip()
        line_number = i

# Display result
print("Longest Line:", longest_line)
print("Line Number:", line_number)
print("Length:", len(longest_line))
