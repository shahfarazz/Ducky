print("Please enter a multi-line string:")
multi_line_string = ""
    # line = input()
line = """Ducky, the user wishes to learn about {topic}. Please provide a concise and informative explanation on the topic, including any relevant coding examples or practices. Ensure that the information is accessible to beginners yet valuable for more experienced coders as well."""
if line:
    multi_line_string += line + "\n"
# Replace newline characters with "\n"
one_line_string = multi_line_string.replace("\n", "\\n")

print("The converted one line string is:")
print(one_line_string)