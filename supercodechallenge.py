## Load pandas and re (regular expressions) to solve this challenge
## pandas for data manipulation and re for cleaning airline codes
import pandas as pd
import re

## Import io for its StringIO class which allows us to create an in-memory text stream:
import io

## We are given the following data:
data = 'Airline Code;DelayTimes;FlightCodes;To_From\nAir Canada (!);[21, 40];20015.0;WAterLoo_NEWYork\n<Air France> (12);[];;Montreal_TORONTO\n(Porter Airways. );[60, 22, 87];20035.0;CALgary_Ottawa\n12. Air France;[78, 66];;Ottawa_VANcouvER\n""".\\.Lufthansa.\\.""";[12, 33];20055.0;london_MONTreal\n'

## Read the CSV data from data into a pd.DataFrame and use io.StringIO to create a file-like
##  object from the string. We should also specify the separator and line terminator.
df = pd.read_csv(io.StringIO(data), sep = ";", line_terminator = "\n")

## We can define a function that leverages re to clean airline codes by removing any non-word
##  characters (barring whistepace) and then stripping any leading or trailing whitespace.
def clean_airline_code(airline_code):
    return re.sub(r'[^\w\s]', '', airline_code).strip()

## Apply clean_airline_code to the 'Airline Code' column, as follows:
df['Airline Code'] = df['Airline Code'].apply(clean_airline_code)

## Assume that FlightCodes are not necessarily in sequence. If they are, then we would
##  leverage the commented portion to proceed further:
'''
## Find the minimum value in the 'FlightCodes' column of df:
min_flight_code = df['FlightCodes'].min()
## Find the maximum value of the 'FlightCodes' column of df:
max_flight_code = df['FlightCodes'].max()
## Generate a complete series of flight codes from the minimum to the maximum value with a step of 10:
complete_flight_codes = pd.Series(range(int(min_flight_code), int(max_flight_code) + 1, 10))
## Fill the missing values in the 'FlightCodes' column with values from the complete series.
## Note that the complete series is truncated to the length of df to match the number of rows.
df['FlightCodes'] = df['FlightCodes'].fillna(complete_flight_codes[:len(df)])
## Convert the 'FlightCodes' column to integer type to ensure it contains only whole numbers:
df['FlightCodes'] = df['FlightCodes'].astype(int)
'''

## With the assumption that the FlightCodes are not necessarily in sequence, we can leverage the
##  interpolate method that uses interpolation to fill missing values. In particular, when we set
##  method = 'linear', we want that the missing values be filled with a linear interpolation between
##  surrounding values. Hence, a row with 1010 above and 1030 below as FlightCode will have a FlightCode
##  of 1020. Note that this example uses interpolation from information below as well as information
##  above the row of interest. Thus, we will be setting limit_direction = 'both' to achieve this.
## Add the .astype(int) at the end to ensure that the column FlightCodes only contains integers.
df['FlightCodes'] = df['FlightCodes'].interpolate(method = 'linear', limit_direction = 'both').astype(int)

## Leverage the str.split method to split the string values in the To_From column based on the '_'
##  character. We set expand = True because we need the result to be a DataFrame with multiple columns
##  (in this case, the columns are 'From' and 'To').
df[['From', 'To']] = df['To_From'].str.split('_', expand = True)

## If we want to convert the two columns to title case, we would proceed with the commented portion:
'''
df['From'] = df['From'].str.title()
df['To'] = df['To'].str.title()
'''

## If we want to convert the two columns to fully capital case, we would proceed as follows:
df['From'] = df['From'].str.upper()
df['To'] = df['To'].str.upper()

## We will now drop the original 'To_From' column from df as follows:
df = df.drop('To_From', axis = 1)

## Note that axis = 1 means to drop a column and axis = 0 means to drop a row.

print(df.head(10)) # Print the first 10 of the new DataFrame df.

