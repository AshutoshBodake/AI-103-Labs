from addition import add
from multiplication import multiply
from ResourceAndOpenAI import chat


# result_addition = add(10, 5)
# result_multiplication = multiply(10, 5)

chat()

# print("Addition:", result_addition)
# print("Multiplication:", result_multiplication)

# def main():
#     x, y = 5, 3
#     print(f"{x} + {y} = {add(x, y)}")
#     print(f"{x} * {y} = {multiply(x, y)}")


# if __name__ == "__main__":
#     main()

# So if __name__ == "__main__": 
# means "only run this code when the file is executed "
# "directly, not when it's imported elsewhere."

# In your case: it calls main() when you run python main.py,
# but if some other script did import main, main() would not
# auto-run — the other script would decide when to call it.