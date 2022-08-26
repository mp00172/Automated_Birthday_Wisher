# 1. Update the birthdays.csv
# 2. Check if today matches a birthday in the birthdays.csv
# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name
# from birthdays.csv
# 4. Send the letter generated in step 3 to that person's email address.


import random
import smtplib
import datetime as dt
import csv

MY_EMAIL = "martin.pytest@yahoo.com"
MY_PASSWORD = "peemwvunfxvcsmzs"
MY_EMAIL_SMTP = "smtp.mail.yahoo.com"
SMTP_PORT = 587


def get_todays_date():
	now = dt.datetime.now()
	return now.day, now.month


def get_data_from_file():
	with open("birthdays.csv", newline="") as csvfile:
		data = csv.reader(csvfile)
		return [row for row in data if row[-1].isnumeric()]


def get_birthdays(data, todays_date):
	return [entry for entry in data if (int(entry[-1]) == todays_date[0] and int(entry[-2]) == todays_date[1])]


def generate_random_letter(name):
	with open(f"letter_{random.randint(1, 3)}.txt", "r") as letter_file:
		letter = letter_file.readlines()
	string_to_return = ""
	for line in letter:
		string_to_return += line
	return string_to_return.replace("[NAME]", name)


def send_email_wish(smtp, port, my_email, my_password, dest_email, message):
	with smtplib.SMTP(smtp, port) as connection:
		connection.starttls()
		connection.login(user=my_email, password=my_password)
		connection.sendmail(from_addr=my_email,
							to_addrs=dest_email,
							msg="Subject:Happy Birthday! :)\n\n"
								"{}".format(message))


todays_date = get_todays_date()
data = get_data_from_file()
birthdays = get_birthdays(data, todays_date)

for birthday in birthdays:
	send_email_wish(smtp=MY_EMAIL_SMTP,
					port=SMTP_PORT,
					my_email=MY_EMAIL,
					my_password=MY_PASSWORD,
					dest_email=birthday[1],
					message=generate_random_letter(birthday[0]))

# The Automated_Birthday_Wisher is supposed to run in the cloud, every day at given time.
