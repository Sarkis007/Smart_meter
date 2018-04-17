import json
import datetime


def load_sm_setup():
    with open('sm_setup.json') as data_file:
        sm_setup = json.load(data_file)
        conv_matrix = sm_setup["sm_setup"]["conv_matrix"]
        return conv_matrix


def load_sm_data():
    try:
        with open('sm_data.json') as data_file:
            sm_data = json.load(data_file)
            return sm_data
    except:
        filex = open('sm_data.json', "w")
        filex.write('{"home":{"water": {}, "gas": {},"electricity":{}}}')
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
        except:
            print "Invalid input"
            x = date_input("The date should be as 'yyyy-mm-dd'")
            return x


def operation(sm_data, conv_matrix):
    while True:
        print "1- Add a new measurement"
        print "2- Check your usage"
        print "3- Exit"
        x = raw_input()
        if x == '1':
            add_measurements(sm_data)
            print "please choose other operation or enter 3 to exit"
        elif x == '2':
            usage_check(sm_data, conv_matrix)
        elif x == '3':
            print "Thank you"
            print "Have a nice day"
            exit()

        else:
            print "invalid input, please enter 1 or 2 or 3"


def add_measurements(sm_data):
    utility = raw_input("Please select the utility measurement you want to add 'gas' 'water' or 'electricity'")
    while True:
        if utility == 'gas' or utility == 'water' or utility == 'electricity':
            sentence = "please insert the date as 'yyyy-mm-dd' or just type 'today' "
            date = date_input(sentence)
            new_measurement = {"home": {utility: {date: {"read": {}}}}}
            while True:
                try:
                    while True:
                        read = input('please enter meter read for '+str(utility)+" on "+str(date))
                        if len(str(read)) == 5:
                            new_measurement["home"][utility][date]["read"] = read
                            save_measurements(new_measurement, utility, sm_data, date)
                            print "measurement added successfully"
                            return utility, date, read
                        else:
                            print "the length should be 5 numbers, please try again"
                except:
                    print "the input should be a number, please try again"
        else:
            utility = raw_input("Invalid input, please enter 'gas' 'water' or 'electricity'")


def utility_unit(utility):
    if utility == 'gas' or utility == 'water':
        return u'm\u00b3'
    elif utility == 'electricity':
        return 'Kwh'


def usage_check(sm_data, conv_matrix):
    utility = raw_input("please select the utility you want to check 'gas' 'water' or 'electricity'")
    while True:
        if utility == 'gas' or utility == 'water' or utility == 'electricity':

            if len(sm_data["home"][utility]) >= 2:
                print"saved data for " + utility + " utility are the following:"
                n = 1
                for key in sm_data["home"][utility]:
                    print str(n) + '- on ' + str(key) + '  -  ' + str(sm_data["home"][utility][key]["read"]) + ' ' +\
                          utility_unit(utility)
                    n = n+1
                print "Enter any two dates to calculate the usage"

                while True:
                    first_date = date_input("please enter the first date you want to add as 'yyyy-mm-dd'")
                    while True:
                        if first_date in sm_data["home"][utility]:
                            break
                        else:
                            first_date = date_input("The date you entered is not in the data," 
                                                    " please enter the date again")
                    second_date = date_input("please enter the second date you want to add as 'yyyy-mm-dd'")
                    while True:
                        if second_date in sm_data["home"][utility]:
                            break
                        else:
                            second_date = date_input("The date you entered is not in the data,"
                                                     " please enter the date again")
                    first_read = sm_data["home"][utility][first_date]["read"]
                    second_read = sm_data["home"][utility][second_date]["read"]
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
                print "There are " + str(len(sm_data["home"][utility])) + " reading" + " for " + utility + " utility"
                print "There should be at least two readings"
                print "Please select other operation"
                operation(sm_data, conv_matrix)
        else:
            utility = raw_input("Invalid input, please enter 'gas' 'water' or 'electricity'")


def save_measurements(new_measurement, utility, sm_data, date):
    sm_data["home"][utility][date] = new_measurement["home"][utility][date]
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
