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
        file.write('{"home":{ "water": { "date": {}, "read": {} }, "gas": { "date": {}, "read": {} }, '
                   '"electricity": { "date": {}, "read": {} } }}')
        file.close()
        with open('sm_data.json') as data_file:
            sm_data = json.load(data_file)
            return sm_data


def validate():
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
            x = validate()
            return x


def operation():
    while True:
        try:
            print "1- add a new measurement"
            print "2- check your usage"
            x = input("please select one of the operations above, enter 1 or 2 or 3")
            if x == 1:
                print "" #1add_measurements()
                while True:
                    try:
                        print ("Do you want to do other operations ?")
                        print ("Please enter 'y' for yes and 'n' for no")
                        repeat = raw_input()
                        if repeat == 'y':
                            operation()
                        elif repeat == 'n':
                            print "Thank you"
                            print "Have a nice day"
                            break  # BUG not breaking two whiles
                        else:
                            print "invalid input please select 'y' or 'n'"
                    except:
                        print "invalid input please select 'y' for yes and 'n' for no"
                break
            elif x == 2:
                print ""
            else:
                print "invalid input"
        except:
            print "invalid input"



def add_measurements():
    print "please select the utility measurement you want to add"
    while True:
        utility = raw_input("'gas' 'water' or 'electricity'")
        if utility == 'gas' or utility == 'water' or utility == 'electricity':
            date = validate()
            while True:
                try:
                    while True:
                        read = input('please enter meter read for '+str(utility)+" on "+str(date))
                        if len(str(read)) == 5:
                            print "measurement added successfully"
                            return utility, date, read
                        else:
                            print "the length should be 5 numbers, please try again"
                except:
                    print "the input should be a number, please try again"
        else:
            print "please select 'gas' 'water' or 'electricity'"




def main():
    print "Welcome to Smart Meter"
    conv_matrix = load_sm_setup()
    sm_data = load_sm_data()
    operation()
main()