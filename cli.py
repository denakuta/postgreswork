def ask_yes_no(question):
    while True:
        answer = input(question + " (y/n): ").lower()

        if answer in ("y", "n"):
            return answer == "y"

        print('only \'y\' or \'n\' allowed')
