from csv import reader
import re


def main():
    # reading csv file
    with open('data.csv', 'r') as read_obj:

        csv_reader = reader(read_obj)
        emails_to_send = []

        for row in csv_reader:
            if row != []:
                if "\tLucas\t\t" in str(row[0]):
                    if "email sent" not in str(row[0]):
                        emails_to_send.append(str(row[0]))

    names = []
    emails = []
    for email in emails_to_send:
        name = re.search(".*?(?=\s{2})", email).group(0)
        name = name.split("\t")[0]
        names.append(name)
        email = re.search(
            '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email).group(0)
        emails.append(email)

    if len(names) != len(emails):
        return "error"

    if names == []:
        f = open("emails_to_write.csv", "w")
        f.write("No emails to write!")
        f.close()
        return

    f = open("emails_to_write.csv", "w")
    for i in range(len(names)):
        # write template email and insert company name when appropriate
        f.write("EMAIL: " + emails[i])
        f.write("\n")
        f.write("Template.......")
        f.write("\n")
        f.write("\n")

    f.close()


if __name__ == "__main__":
    main()
