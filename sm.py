import json
import datetime


def load_sm_setup():
    try:
        with open('sm_setup.json') as data_file:
            sm_setup = json.load(data_file)
            conv_matrix = sm_setup["sm_setup"]["conv_matrix"]
            return conv_matrix
    except (IOError, ValueError):
        filex = open('sm_setup.json', "w")
        filex.write('{ "sm_setup": { "conv_matrix": { "water": 194.3, "gas": 72, "electricity": 21.32 } } }')
        filex.close()
        with open('sm_setup.json') as data_file:
            sm_setup = json.load(data_file)
            conv_matrix = sm_setup["sm_setup"]["conv_matrix"]
            return conv_matrix


def load_sm_data():
    try:
        with open('sm_data.json') as data_file:
            sm_data = json.load(data_file)
            return sm_data
    except (IOError, ValueError):
        filex = open('sm_data.json', "w")
        filex.write('{"Home":{"water": {}, "gas": {},"electricity":{}}, "Work":{"water": {}, "gas": {},'
                    '"electricity":{}}, "Other":{"water": {}, "gas": {},"electricity":{}}}')
        filex.close()
        with open('sm_data.json') as data_file:
            sm_data = json.load(data_file)
            return sm_data


def date_input(sentence):
    now = datetime.datetime.now()
    date = raw_input(sentence)
    if date == 'today':
        date = str(now.strftime("%Y-%m-%d"))
        return date
    else:
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            return date
        except ValueError:
            print "Invalid input"
            x = date_input("The date should be as 'yyyy-mm-dd'")
            return x


def place_info(sm_data):
    n = 1
    for key in sm_data:
        print n, '-', key
        n = n + 1
    place = raw_input()
    while True:
        if place == '1':
            place = 'Home'
            return place
        elif place == '2':
            place = 'Work'
            return place
        elif place == '3':
            place = 'Other'
            return place
        else:
            place = raw_input("please enter 1 or 2 or 3")


def utility_info():
    print "please select one of the following utilities"
    print "1- Electricity"
    print "2- Water"
    print "3- Gas"
    utility = raw_input()
    while True:
        if utility == '1':
            utility = 'electricity'
            return utility
        elif utility == '2':
            utility = 'water'
            return utility
        elif utility == '3':
            utility = 'gas'
            return utility
        else:
            utility = raw_input("please enter 1 or 2 or 3")


def operation(sm_data, conv_matrix):
    while True:
        print "1- Add a new measurement"
        print "2- Check your usage"
        print "3- Edit the data"
        print "4- Exit"
        x = raw_input()
        if x == '1':
            print "Please select for which place you want to add a new measurement"
            place = place_info(sm_data)
            utility = utility_info()
            add_measurements(sm_data, place, utility, conv_matrix)
            print "Please choose other operation or enter 4 to exit"
        elif x == '2':
            print "Please select for which place you want to check your usage"
            place = place_info(sm_data)
            utility = utility_info()
            usage_check(sm_data, conv_matrix, place, utility)
        elif x == '3':
            print "please select for which place you want to edit the data"
            place = place_info(sm_data)
            utility = utility_info()
            edit_data(sm_data, conv_matrix, place, utility)
        elif x == '4':
            print "Thank you"
            print "Have a nice day"
            exit()
        else:
            print "invalid input, please enter 1 or 2 or 3"


def add_measurements(sm_data, place, utility, conv_matrix):
    date = date_input("please insert the date as yyyy-mm-dd or just type 'today' ")
    new_measurement = {place: {utility: {date: {"read": {}}}}}
    if date not in sm_data[place][utility]:
        while True:
            try:
                read = input('please enter meter read for '+str(utility)+" on " + date)
                if len(str(read)) <= 5:
                    new_measurement[place][utility][date]["read"] = read
                    save_measurements(new_measurement, utility, sm_data, date, place)
                    print "measurement added successfully"
                    return utility, date, read
                else:
                    print "the length should not be more than 5 numbers, please try again"
            except NameError:
                print "Invalid input, your input should be only numbers"
    else:
        print "The date you entered already exists if you want to edit it please enter 3 or choose other operation"
        operation(sm_data, conv_matrix)


def utility_unit(utility):
    if utility == 'gas' or utility == 'water':
        return u'm\u00b3'
    elif utility == 'electricity':
        return 'Kwh'


def usage_check(sm_data, conv_matrix, place, utility):
    if len(sm_data[place][utility]) >= 2:
        print"saved data for " + utility + " utility are the following:"
        n = 1
        for key in sm_data[place][utility]:
            print str(n) + '- on ' + str(key) + '  -  ' +\
                    str(sm_data[place][utility][key]["read"]) + ' ' + utility_unit(utility)
            n = n + 1
        print "Enter any two dates to calculate the usage"
        while True:
            first_date = date_input("please enter the first date you want to add as 'yyyy-mm-dd'")
            while True:
                if first_date in sm_data[place][utility]:
                    break
                else:
                    first_date = date_input("The date you entered is not in the data," 
                                            " please enter the date again")
            second_date = date_input("please enter the second date you want to add as 'yyyy-mm-dd'")
            while True:
                if second_date in sm_data[place][utility]:
                    break
                else:
                    second_date = date_input("The date you entered is not in the data,"
                                             " please enter the date again")
            first_read = sm_data[place][utility][first_date]["read"]
            second_read = sm_data[place][utility][second_date]["read"]
            if first_date > second_date and first_read > second_read or first_date < second_date and first_read\
                    < second_read:
                used_amount = abs(int(first_read - second_read))
                from datetime import datetime
                date_format = "%Y-%m-%d"
                a = datetime.strptime(first_date, date_format)
                b = datetime.strptime(second_date, date_format)
                delta = abs(b - a)
                used_days = delta.days
                cost = used_amount*conv_matrix[utility]
                print "The amount of", utility, "used in", used_days, "days is",\
                    used_amount, utility_unit(utility)
                print "which's cost for", used_days, "days is", cost, "Drams"
                if used_days > 30:
                    print "Approximately", int((30*cost)/used_days), "Drams per month"
                else:
                    print "Approximately", int(cost/used_days), "Drams per Day"
                x = raw_input("Do you want to do other operations enter 'y' for yes and 'n' to exit")
                while True:
                    if x == 'y':
                        print "please select one of the following"
                        operation(sm_data, conv_matrix)
                    elif x == 'n':
                        print "Thank you"
                        print "Have a nice day"
                        exit()
                    else:
                        x = raw_input("Invalid input, please enter 'y' for yes and 'n' to exit")
            else:
                print first_date + '  -  ', first_read
                print second_date + '  -  ', second_read
                if first_date > second_date:
                    print "the usage for " + second_date + " is bigger than the usage of " + first_date
                    print "which makes no sense, please check the readings for the dates"
                if first_date < second_date:
                    print "the usage for " + first_date + " is bigger than the usage of " + second_date
                    print "which makes no sense, please check the readings for the dates"
                print "if you want to do other operations select one or exit"
                operation(sm_data, conv_matrix)
    else:
        print "There are " + str(len(sm_data[place][utility])) + " reading" + " for " + utility + " utility"
        print "There should be at least two readings"
        print "Please select other operation"
        operation(sm_data, conv_matrix)


def edit_data(sm_data, conv_matrix, place, utility):
    if len(sm_data[place][utility]) >= 1:
        print"saved data for " + utility + " utility are the following:"
        n = 1
        for key in sm_data[place][utility]:
            print str(n) + '- on ' + str(key) + '  -  ' + str(sm_data[place][utility][key]["read"]) + \
                    ' ' + utility_unit(utility)
            n = n + 1
        date_select = date_input("please select one of the dates above to edit")
        while True:
            if date_select in sm_data[place][utility]:
                break
            else:
                date_select = date_input("The date you entered is not in the data, please enter the date again")
        edit_or_delete = raw_input("Do you want to delete it or change it ?")
        while True:
            if edit_or_delete == 'change':
                while True:
                    try:
                        read = input(
                            'please enter the new meter read for ' + str(utility) + " on " + str(date_select))
                        if len(str(read)) <= 5:
                            sm_data[place][utility][date_select]["read"] = read
                            save_measurements(sm_data, utility, sm_data, date_select, place)
                            print "measurement changed successfully"
                            operation(sm_data, conv_matrix)
                        else:
                            print ("Invalid input, your input should not be more than 5 digits")
                    except NameError:
                        print "Invalid input, your input should be only numbers"
            elif edit_or_delete == 'delete':
                del sm_data[place][utility][date_select]
                save_measurements(sm_data, utility, sm_data, date_select, place)
                print "measurement deleted successfully"
                operation(sm_data, conv_matrix)
            else:
                edit_or_delete = raw_input("Invalid input, please enter 'edit' or 'delete'")
    else:
        print "There are no readings for", utility, "utility to edit"
        operation(sm_data, conv_matrix)


def save_measurements(new_measurement, utility, sm_data, date, place):
    try:
        sm_data[place][utility][date] = new_measurement[place][utility][date]
    except KeyError:
        sm_data[place][utility] = new_measurement[place][utility]
    filex = open("sm_data.json", "w")
    filex.write(json.dumps(sm_data))
    filex.close()


def main():

    conv_matrix = load_sm_setup()
    sm_data = load_sm_data()
    print "Welcome to Smart Meter"
    print "Please select one of the following operations"
    operation(sm_data, conv_matrix)


main()
