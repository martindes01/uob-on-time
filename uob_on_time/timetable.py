"""Online timetable classes.

This module contains the classes necessary to navigate and scrape events from the online timetable at `https://onlinetimetables.bham.ac.uk/Timetable/current_academic_year_2/`.

Classes
-------
Event
    Stores details of an online timetable event.
Timetable
    Navigates online timetable and scrapes events.

"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from itertools import chain


default_url = 'https://onlinetimetables.bham.ac.uk/Timetable/current_academic_year_2/default.aspx'
"""The URL of the online timetable filter form."""

login_url = 'https://onlinetimetables.bham.ac.uk/Timetable/current_academic_year_2/login.aspx'
"""The URL of the online timetable site login."""

timeout = 10
"""The default timeout period in seconds used by `WebDriverWait` objects in this module."""

timetable_url = 'https://onlinetimetables.bham.ac.uk/Timetable/current_academic_year_2/showtimetable.aspx'
"""The URL of the online timetable page."""


# Classes

class Event:
    """Class for storing details of an online timetable event.

    Attributes
    ----------
    date : str
        The date of the event in the format '%-d %b %Y'.
    activity : str
        The summary of the event.
    type : str
        The type of the event.
    start : str
        The start time of the event in the format '%-H:%M'.
    end : str
        The end time of the event in the format '%-H:%M'.
    room : str
        The venue of the event.
    staff : str
        The names of staff present at the event.
    department : str
        The name of the department in charge of the event.

    See Also
    --------
    datetime.strftime

    """

    def __init__(
            self,
            date: str='',
            activity: str='Untitled activity',
            type: str='Other',
            start: str='9:00',
            end: str='19:00',
            room: str='TBC',
            staff: str='TBC',
            department: str='N/A'
        ):
        self.date = date
        self.activity = activity
        self.type = type
        self.start = start
        self.end = end
        self.room = room
        self.staff = staff
        self.department = department

    def __str__(self):
        return f'{self.activity} of type {self.type} on {self.date} from {self.start} to {self.end} in {self.room} with {self.staff} of {self.department}.'

class Timetable:
    """Class for navigating online timetable site and scraping events.

    Attributes
    ----------
    driver : webdriver
        The web driver used to navigate the online timetable site.
    events : List[Event]
        The list of `Event` objects retrieved from this `Timetable` when `scrape()` is called.

    Methods
    -------
    load()
        Load online timetable page.
    login(username, password)
        Log into online timetable site.
    scrape()
        Retrieve event data from online timetable.

    """

    def __init__(self):
        # Create instance of Chrome driver in incognito mode
        options = webdriver.ChromeOptions()
        options.add_argument('--incognito')
        self.driver = webdriver.Chrome(options=options)

        # List to hold scraped events
        self.events = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Close Chrome driver
        self.driver.quit()

    def __str__(self):
        string = f'{len(self.events)} events scraped from online timetable:'
        for event in self.events:
            string += f'\n-- {event}'
        return string

    def load(self) -> bool:
        """Load the online timetable page into the web driver of this `Timetable`.

        Fill timetable filter form using most inclusive values and navigate to timetable page.

        Returns
        -------
        bool
            True if successful, False otherwise.

        Raises
        ------
        NoSuchElementException
            If `driver` url is not `default_url` or online timetable site format has changed.

        See Also
        --------
        default_url
        login

        Notes
        -----
        `login(username, password)` must be called first.

        """

        # Load timetable filter form
        try:
            self.driver.execute_script('__doPostBack(arguments[0], arguments[1])', 'LinkBtn_mystudentset', '')
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.text_to_be_present_in_element((By.ID, 'tFilterTitle'), 'My Timetable'))
        except:
            return False

        # Select all weeks
        week_select = Select(self.driver.find_element_by_name('lbWeeks'))
        week_select.select_by_visible_text('*All Term Time')
        for i in chain(range(1, 6), range(44, 53)):
            week_select.select_by_value(' ' + str(i))

        # Select all days
        day_select = Select(self.driver.find_element_by_name('lbDays'))
        day_select.select_by_visible_text('All Week')

        # Select all periods
        period_select = Select(self.driver.find_element_by_name('dlPeriod'))
        period_select.select_by_visible_text('All Day (08:00 - 22:00)')

        # Select list with calendar dates type
        type_select = Select(self.driver.find_element_by_name('dlType'))
        type_select.select_by_visible_text('List Timetable (with calendar dates)')

        # Submit form
        self.driver.find_element_by_name('bGetTimetable').click()

        # Wait for navigation to timetable URL
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.url_to_be(timetable_url))
            return True
        except:
            return False

    # Log into timetable site with specified username and password
    def login(self, username: str, password: str) -> bool:
        """Log into online timetable site as user with specified username and password.

        Parameters
        ----------
        username : str
            The username of the user.
        password : str
            The password of the user.

        Returns
        -------
        bool
            True if successful, False otherwise.

        Raises
        ------
        NoSuchElementException
            If `driver` url is not `login_url` or online timetable site format has changed.

        See Also
        --------
        login_url

        """

        # Navigate to login page
        self.driver.get(login_url)

        # Input username
        username_input = self.driver.find_element_by_name('tUserName')
        username_input.clear()
        username_input.send_keys(username)

        # Input password and return
        password_input = self.driver.find_element_by_name('tPassword')
        password_input.clear()
        password_input.send_keys(password, Keys.RETURN)

        # Wait for navigation to default URL
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.url_to_be(default_url))
            return True
        except:
            return False

    def scrape(self) -> None:
        """Retrieve event data from the online timetable page loaded into the web driver of this `Template`.

        Populate the `events` list attribute of this `Timetable` with `Event` objects created using text present in the online timetable page.

        Raises
        ------
        NoSuchElementException
            If `driver` url is not `timetable_url` or online timetable site format has changed.

        See Also
        --------
        timetable_url
        login, load

        Notes
        -----
        `login(username, password)` and `load()` must be called first.

        """

        # Iterate through event rows
        for event_tr in self.driver.find_elements_by_css_selector('.spreadsheet tr:not(.columnTitles)'):
            # Unpack event data cells
            date_td, activity_td, type_td, start_td, end_td, room_td, staff_td, department_td = event_tr.find_elements_by_tag_name('td')

            # Create event and append to events list
            self.events.append(
                Event(
                    date_td.text,
                    activity_td.text,
                    type_td.text,
                    start_td.text,
                    end_td.text,
                    room_td.text,
                    staff_td.text,
                    department_td.text
                )
            )
