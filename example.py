"""Online timetable to Google Calender converter.

Prompts user for UoB username and password and logs into online timetable site.
Loads online timetable and scrapes events.
Events are added to Google Calendar.

"""

from uob_on_time.timetable import Timetable

import getpass


def main():
    # Create timetable object
    with Timetable() as t:
        # Log into online timetable site
        while True:
            username = input('Enter UoB username (e.g. abc123): ')
            password = getpass.getpass('Enter UoB password (hidden): ')
            if t.login(username, password):
                # Break loop if login successful
                print(f'Logged in as {username}.')
                break
            else:
                print('Incorrect username or password. Try again.')

        # Load timetable
        print('Loading timetable...')
        if t.load():
            # Scrape and print timetable
            print('Scraping timetable...')
            t.scrape()
            print(t)
        else:
            print('Timeout. Failed to load timetable.')

        # Timetable destroyed on exit from with statement
        print('Logging out...')

    print('Finished.')


if __name__ == "__main__":
    main()
