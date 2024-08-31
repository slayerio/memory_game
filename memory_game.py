print('Welcome to my memory game!')
print('in this game that are 6 groups (A-F)) couple of every card.')
print('you have to pick two numbers between 0-11, trying to guess if both of the numbers')
print('are the same card. ')
print("to win- you have to guess all groups.")
print('Good luck!')

cards_to_nums = {
    'A': (1, 11),
    'B': (2, 7),
    'C': (3, 10),
    'D': (0, 9),
    'E': (4, 5),
    'F': (6, 8),
}

picked_groups = []


def find_key(num: int) -> str:
    for key, value in cards_to_nums.items():
        if num in value:
            return key
    return None


def picked_numbers(a, b: int) -> str:
    group_a = find_key(a)
    group_b = find_key(b)

    if group_a and group_b:
        if group_a == group_b:
            if group_a not in picked_groups:
                picked_groups.append(group_a)
                return f'correct! you got group {group_a}'
            else:
                return f'{group_a} already been picked'
        else:
            return f'incorrect, you got {a} in {group_a} and {b} in {group_b}'
    else:
        return 'one or both the numbers are not in any group'


while len(picked_groups) < len(cards_to_nums):
    try:
        a = int(input("pick a number between 0-11:"))
        b = int(input("pick a number between 0-11:"))

        if not (0 <= a <= 11) or not (0 <= b <= 11):
            print('not between 0-11. try again')
            continue

        print(picked_numbers(a, b))

    except ValueError:
        print('pick valid number 0-11')


print("well done! you finished the game!")
