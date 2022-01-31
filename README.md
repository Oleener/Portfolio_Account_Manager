# Portfolio_Account_Manager
This application is a stock and cryptocurrency portfolio management tool that allows the user to create, delete, edit, and manage different portfolios as well as analyze their performance after creating a user account on the application. After verifying their email address, the user is then able to receive even better insights with deeper analysis features.

---

## Technologies

The project leverages Pyhton 3.7 with the following packages:

* [ALPACA](https://github.com/alpacahq/alpaca-trade-api-python#:~:text=alpaca%2Dtrade%2Dapi%2Dpython%20is%20a%20python%20library%20for,REST%20and%20streaming%20data%20interfaces.) - Commission free trading API. 
* [dash](https://github.com/plotly/dash) - An open-source Python framework used for building analytical web applications.
* [dash dcc](https://dash.plotly.com/dash-core-components) - An upload component that allows users to create elements such as graphs, dropdowns or sliders. 
* [dash html](https://github.com/plotly/dash-html-components) - Dash provides HTML classes which enables the suer to generate HTML content with python. 
* [datetime](https://www.geeksforgeeks.org/python-datetime-module/#:~:text=Python%20Datetime%20module%20supplies%20classes,and%20not%20string%20or%20timestamps.) - Supplies classes to work with date and time.
* [dotenv](https://github.com/theskumar/python-dotenv#:~:text=Python%2Ddotenv%20reads%20key%2Dvalue,following%20the%2012%2Dfactor%20principles.) - A zero-dependency module that loads environment variables from a .env file into process.env. Storing configuration in the environment separate from code.
* [EmailMessage](https://docs.python.org/3/library/email.message.html#:~:text=EmailMessage%20provides%20the%20core%20functionality,referred%20to%20as%20the%20content) - Provides the core functionality for setting and querying header fields, for accessing message bodies, and for creating or modifying structured messages.
* [fire](https://github.com/google/python-fire) - For the command line interface, help page, and entrypoint.
* [hashlib](https://www.askpython.com/python-modules/python-hashlib-module#:~:text=The%20Python%20hashlib%20module%20is,very%20difficult%20to%20decrypt%20it.) - An interface for hashing messages easily in an encrypted format.
* [json](https://www.geeksforgeeks.org/python-json/#:~:text=JSON%20JavaScript%20Object%20Notation%20is,built%2Din%20package%20called%20json.) - Format for structuring data used for storing and transferring data between the browser and the server.
* [NumPy](https://numpy.org/doc/stable/user/absolute_beginners.html#:~:text=NumPy%20can%20be%20used%20to,on%20these%20arrays%20and%20matrices.) - Used to perform a wide variety of mathematical operations on arrays.
* [os](https://www.geeksforgeeks.org/os-module-python-examples/) - Provides functions for creating/removing a directory, fetching its contents, changing and identifying the current directory.
* [Pandas](https://github.com/pandas-dev/pandas#:~:text=data%20analysis%20toolkit-,What%20is%20it%3F,world%20data%20analysis%20in%20Python.) - For data manipulation and analysis 
* [plotly](https://github.com/plotly/plotly.py) - Makes interactive, publication-quality graphs
* [questionary](https://github.com/tmbo/questionary) - For interactive user prompts and dialogs
* [RE](https://docs.python.org/3/howto/regex.html) - Used to match strings of text such as particular characters, words, or patterns of characters
* [requests](https://www.geeksforgeeks.org/http-request-methods-python-requests/) - Allow you to send/access HTTP/1.1 requests using Python
* [SMTP](https://docs.python.org/3/library/smtplib.html#:~:text=The%20smtplib%20module%20defines%20an,1869%20(SMTP%20Service%20Extensions).) - Defines an SMTP client session object that can be used to send mail to any internet machine with an SMTP or ESMTP listener daemon.
* [SQL](https://github.com/tiangolo/sqlmodel) - A programming language used for managing or querying data stored in a relational database management system.
* [sys](https://docs.python.org/3/library/sys.html) - Provides functions and variables that are used to manipulate different parts of the python runtime enviorment.

---

## Installation Guide 

Before running the application first install the following dependencies.

```
Install Anaconda Package
```
ALPACA - ``` pip install alpaca-trade-api ```

Dash - ``` pip install dash ```

DateTime - ``` pip install DateTime ```

Dotenv - ``` pip install python-dotenv ```

fire - ``` pip install fire ```

json - ``` conda install -c jmcmurray json ```

NumPy - ``` pip install numpy  ```

Pandas - ``` pip install pandas ```

Plotly - ``` pip install plotly==5.5.0 ```

questionary - ``` pip install questionary ```

RE - ``` pip install regex ```

Requests - ``` conda install -c anaconda requests ```

SMTP - ``` pip install smtplib ```

SQL - ``` pip install SQLAlchemy ```

---

## Usage 

To use the Portfolio account manager application simply clone the repository and run the **app.py** with:

```python
python app.py
```
Upon launching the portfolio account manager application you will be greated with the following prompt.

![1](https://github.com/Oleener/Portfolio_Account_Manager/blob/olena_dev/Instructions/1.png)

To use the application you will need to create a user profile via the ```Sign Up``` option. 
If you already have a profile set up proceed using the ```Log In``` option.

Once logged in, an email verification screen will be prompted lettting you know whether your account is verified or not. This screen will also give you the option to verify your account through your email. 

![2](https://github.com/Oleener/Portfolio_Account_Manager/blob/olena_dev/Instructions/2.png) 

After proceeding with email verification, Global Management Mode will be activated which will display the users stock and crypto portfolio.

![3](https://github.com/Oleener/Portfolio_Account_Manager/blob/olena_dev/Instructions/3.png)

Once in the global management mode, the user will have the ability to:

```
Manage Portfolio
Add new Portfolio
```

When the option ```Manage Portfolio``` is selected, the user will have the ability to: 

```
Add new Asset 
Add Existing Asset 
Remove Portfolio
Edit Portfolio
```

The user is able to perform deep portfolio analysis on their portfolio ONLY if their account is verified. 

---

## Presentation

The powerpoint below summerizes the main points of Portfolio Account Manager. 

![powerpoint](https://github.com/Oleener/Portfolio_Account_Manager/blob/olena_dev/Instructions/Fintech%20-%20Project%201.pdf)

---

## Contributors

Brought To you by: 

Olena Shemedyuk (olenashemedyuk@gmail.com)
Kirill Panov (us.kirpa1986@gmail.com)
Isaiah Tensae (isaiahtensae@gmail.com)
Nick Strohm (Strohm241@gmail.com)

---


## License 

MIT

