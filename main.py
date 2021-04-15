import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import json


def load_address_types():
    """
    addresses.txt should be like below
    '{
    "+91XXX": "name1",
    "+91YYY": "name2",
    }'
    """
    with open('addresses.txt') as add_file:
        data = json.load(add_file)
        return data


class SMS:
    address_type = load_address_types()

    def __init__(self, address, type_of_sms, date, message):
        self.address = address
        self.type_of_sms = type_of_sms
        self.epoch_date = date
        self.message = message

        self.date_time = epoch_to_ist(self.epoch_date)

        self.address_to = "Hritwik"
        self.address_from = self.address
        self.set_address()

    def set_address(self):
        if self.address in self.address_type:
            # Means the message is of convo b/w me and xxx
            if self.type_of_sms == '1':  # i received it from xxx
                self.address_from = self.address_type[self.address]
            else:
                self.address_to = self.address_type[self.address]
                self.address_from = "Hritwik"


def convert_to_ms(sec):
    return int(sec) / 1000


def format_to_readable(datetime_time_obj):
    # converts "2019-10-14 03:54:58" to "Mon 14-Oct-2019 03:54 AM"
    formatted_time = datetime_time_obj.strftime('%a %d-%b-%Y %I:%M %p')
    return formatted_time


def add_ist_offset(time, offset="0530"):
    # adds offset to "Mon 14-Oct-2019 03:54 AM", so returns "Mon 14-Oct-2019 09:24 AM"
    with_offset = datetime.strptime(str(time), '%a %d-%b-%Y %I:%M %p') + timedelta(hours=int(offset[:2]),
                                                                                   minutes=int(offset[2:]))
    formatted_with_offset = format_to_readable(with_offset)
    return formatted_with_offset


def epoch_to_ist(epoch_time):
    # converts "1571005498" to "2019-10-14 03:54:58"
    datetime_time = datetime.fromtimestamp(convert_to_ms(epoch_time))
    return add_ist_offset(format_to_readable(datetime_time))


def parseXML(xmlfile):
    # create element tree object
    tree = ET.parse(xmlfile)

    # get root element
    root = tree.getroot()

    sms_arr = []

    for i, sms in enumerate(root.findall('sms')):
        address = sms.get('address')
        type_of_sms = sms.get('type')
        date = sms.get('date')
        message = sms.get('body')

        sms_arr.append(SMS(address, type_of_sms, date, message))

        # print(type_of_sms, epoch_to_ist(date))
        # print(address, ":", message)
        # print()

    return sms_arr


def print_sms(sms_arr):
    with open('sms.txt', 'w+') as myfile:
        for sms in sms_arr:
            myfile.writelines(sms.date_time + ', ' + sms.address_from + ': ' + sms.message + '\n')
            # print(sms_arr[i].address_from, "->", sms_arr[i].address_to)
            # print(sms_arr[i].date_time, end=', ')
            # print(sms_arr[i].address_from, end=': ')
            # print(sms_arr[i].message)


def start():
    sms_file = 'sms.xml'
    sms_arr = parseXML(sms_file)

    sms_arr.sort(key=lambda x: x.epoch_date)
    print_sms(sms_arr)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start()
