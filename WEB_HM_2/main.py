from address_book import address_book
from notes import notes
from birthdays import birthdays
from about_us import about_us
from sort import sort


def main():
    while True:
        print('1. Address book')
        print('2. Notes')
        print('3. Display upcoming birthdays')
        print('4. Sorting file')
        print('5. About us')
        print('0. Exit')
        choice = input('Please choose a function (1-5): ')
        if choice == '1':
            address_book()
        elif choice == '2':
            notes()
        elif choice == '3':
            birthdays()
        elif choice == '4':
            sort()
        elif choice == '5':
            about_us()
        elif choice == '0':
            print('Exiting the program...')
            break
        else:
            print('Invalid choice. Please try again.')


if __name__ == '__main__':
    main()
