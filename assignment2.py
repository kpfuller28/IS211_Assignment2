import argparse
import urllib.request
import logging
import datetime


def downloadData(url):
    """Downloads the data"""
    with urllib.request.urlopen(url) as response:
        response = response.read().decode("utf-8")
    return response


def processData(file_content):
    logger = logging.getLogger("assignment2")
    file_handler = logging.FileHandler("errors.log", mode="a", encoding="utf-8")
    logger.addHandler(file_handler)
    formatter = logging.Formatter(
        "{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
    )
    file_handler.setFormatter(formatter)

    data = {}
    lines = file_content.splitlines()
    for line in lines:
        lineData = line.split(",")
        if lines.index(line) == 0:
            continue
        try:
            date = datetime.datetime.strptime(lineData[2], "%d/%m/%Y")
            data[lineData[0]] = (lineData[1], date)
        except:
            logger.error(
                f"Error processing line#{lines.index(line)+1} for ID #{lineData[0]}"
            )
    return data


def displayPerson(id, personData):
    try:
        person = personData[str(id)]
        name = person[0]
        birthday = person[1].strftime("%Y-%m-%d")
        print(f"Person #{id} is {name} with a birthday of {birthday}")
    except:
        print("No user found with that id")


def main(url):
    print(f"Running main with URL = {url}...")
    try:
        csvData = downloadData(url)
    except Exception as error:
        print("An error occured while downloading the data: ", error)
        return
    personData = processData(csvData)
    while True:
        try:
            id = int(
                input(
                    "What ID would you like to look up? Please enter a valid ID number, or any number less than 1 to exit: "
                )
            )
        except ValueError:
            print("ID must be an integer, try again.")
            continue
        if id <= 0:
            return
        else:
            displayPerson(id, personData)
            continue


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
