# uob-on-time

*Scrape your University of Birmingham timetable and convert it to a Google calendar. Say goodbye to my.bham.ac.uk!*

## About

This project provides a script and corresponding API that allows University of Birmingham students to scrape their personal timetables from the online timetable site accessible from [my.bham.ac.uk](https://www.my.bham.ac.uk/).

This project is compatible with version 2 of the Enterprise Timetabler web application by Scientia Ltd.
The non-personal timetables are hosted [here](https://onlinetimetables.bham.ac.uk/timetable/current_academic_year/default.aspx).

## Getting Started

### Prerequisites

An installation of [Python](https://www.python.org/) version 3.6 or later is required to run the software.

This project currently uses the Google Chrome interface of Selenium WebDriver.
Therefore, an installation of the [Google Chrome](https://www.google.com/chrome/) web browser is required to run the software.

If you wish to use an alternative interface, refer to the [Selenium documentation](https://www.selenium.dev/documentation/).
You will need to redefine the `__init__` method of the `Timetable` class in [timetable.py](uob_on_time/timetable.py).

### Installation

Clone the source from this repository.

```shell
git clone https://github.com/martindes01/uob-on-time.git
cd uob-on-time
```

Create and activate a virtual environment, specifying a suitable path `<path>`.
A common name for the environment directory is `.venv`.

```shell
python3 -m venv <path>
source <path>/Scripts/activate
```

Install the dependencies listed in [requirements.txt](requirements.txt).

```shell
pip install --requirement requirements.txt
```

Download the version of [ChromeDriver](https://chromedriver.chromium.org/) that corresponds to the installed version of Google Chrome.
1. In Google Chrome, navigate to `chrome://version/` and note the version number.
1. Download the corresponding version of ChromeDriver from [here](https://chromedriver.chromium.org/downloads).
1. Add the ChromeDriver executable to the system path or place it in the root directory.

## Usage

The basic workflow is demonstrated in the [example.py](example.py) script, which prompts the user for valid login details, logs into the online timetable site, loads the personal timetable and scrapes it.
This is achieved using the `login`, `load` and `scrape` methods of the `Timetable` class.
As the Google Calendar functionality has yet to be implemented, the scraped timetable is simply printed to standard output in a human-readable format.

```shell
python3 example.py
```

The `Timetable` class is documented in [timetable.py](uob_on_time/timetable.py).

## License

This project is distributed under the terms of the MIT License.
See [LICENSE](LICENSE) for more information.
