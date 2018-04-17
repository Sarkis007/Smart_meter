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
        file = open('sm_data.json', "w")
        file.write('{"home":{"water": {}, "gas": {},"electricity":{}}}')
        file.close()
        with open('sm_data.json') as data_file:
            sm_data = json.load(data_file)
            return sm_data


def date_input():
    now = datetime.datetime.now()
    date = raw_input("please insert the date as 'yyyy-mm-dd' or just type 'today' ")
    if date == 'today':
        date = str(now.strftime("%Y-%m-%d"))
        return date
    else:
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            return date
        except:
            x = date_input()
            return x


def operation(sm_data):
    print "Welcome to Smart Meter"
    print "please select one of the following operations"
    while True:
        print "1- add a new measurement"
        print "2- check your usage"
        print "3- exit"
        x = raw_input()
        if x == '1':
            add_measurements(sm_data)
            print "please choose other operation or enter 3 to exit"
        elif x == '2':
            print ""
        elif x == '3':
            print "Thank you"
            print "Have a nice day"
            break
        else:
            print "invalid input, please enter 1 or 2 or 3"


def add_measurements(sm_data):
    print "please select the utility measurement you want to add"
    while True:
        utility = raw_input("'gas' 'water' or 'electricity'")
        if utility == 'gas' or utility == 'water' or utility == 'electricity':
            date = date_input()
            new_measurement = {"home": {utility: {date: {"read": {}}}}}
            while True:
                try:
                    while True:
                        read = input('please enter meter read for '+str(utility)+" on "+str(date))
                        if len(str(read)) == 5:
                            new_measurement["home"][utility][date]["read"] = read
                            print new_measurement
                            save_measurements(new_measurement, utility, sm_data, date)
                            print "measurement added successfully"
                            return utility, date, read
                        else:
                            print "the length should be 5 numbers, please try again"
                except:
                    print "the input should be a number, please try again"
        else:
            print "please select 'gas' 'water' or 'electricity'"


def save_measurements(new_measurement, utility, sm_data, date):
    sm_data["home"][utility][date] = new_measurement["home"][utility][date]
    file = open("sm_data.json", "w")
    file.write(json.dumps(sm_data))
    file.close()


def main():

    conv_matrix = load_sm_setup()
    sm_data = load_sm_data()
    operation(sm_data)


main()