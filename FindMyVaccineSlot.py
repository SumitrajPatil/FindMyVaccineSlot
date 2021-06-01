import time
import http.client
import json
import smtplib

flag = True
while flag:
    '''FOR EVERY 3 MINS API WILL MAKE A CALL TO FIND SLOTS AVAILABILITY '''
    print("waiting for 3 mins... Have patience")
    time.sleep(180)
    print("3 mins wait ended you can relax")
    conn = http.client.HTTPSConnection("cdn-api.co-vin.in")
    payload = ''
    headers = {}
    '''CHANGE DISTRICT ID WHEREVER YOU STAY'''
    '''TO FIND OUT DISTRICT ID YOU NEED TO MAKE A GET REQUEST TO THIS BELOW PARTICULAR API WHICH WILL FIND OUT STATE ID '''
    '''GET REQUEST TO STATE ID: https://cdn-api.co-vin.in/api/v2/admin/location/states'''
    '''ONCE YOU GET RESPONSE AND YOU SEE STATE ID OF YOUR PARTICULAR STATE, YOU CAN USE THAT STATE ID TO FIND OUT DISTRICT ID WITH BELOW API'''
    '''GET REQUEST TO DISTRICT ID: https://cdn-api.co-vin.in/api/v2/admin/location/districts/{state_id}'''
    '''CHANGE THE DATE FROM WHICH DAY YOU WANT TO LOOK UP FOR VACCINE SLOTS'''
    '''IT WILL CHECK FOR THE SLOTS FOR NEXT 7 DAYS FROM THE DATE YOU HAVE GIVEN IN API'''

    conn.request("GET", "/api/v2/appointment/sessions/public/calendarByDistrict?district_id=264&date=22-05-2021", payload, headers)
    res = conn.getresponse()
    data = res.read()
    new_data = data.decode("utf-8")
    json_data = json.loads(new_data)
    json_arr = json_data['centers']

    '''PROVIDE EMAILS IN LIST TO WHOM YOU NEED TO NOTIFY ABOUT VACCINE SLOTS'''
    email_list = ["patil.sumitraj@gmail.com"]
    for center in json_arr:
        '''CHECK THE CENTER ID WHERE YOU WANT TO BOOK SLOT FROM ABOVE API AND PROVIDE SAME CENTER ID BELOW'''
        if center['center_id'] == 562596:
            center_sess_arr = center['sessions']
            for sess in center_sess_arr:
                print(sess['available_capacity'])
                capacity = sess['available_capacity']
                date = sess['date']
                if capacity > 1:
                    s = smtplib.SMTP('smtp.gmail.com', 587)
                    s.starttls()
                    '''YOU NEED TO PROVIDE EMAIL ID AND PASSWORD FROM WHICH EMAIL ID YOU WANT TO SEND NOTIFICATION'''
                    s.login("EMAILID@gmail.com", "PASSWORD")
                    message = "There are "+str(capacity) + " Slots available on " + date + " book it ASAP by visiting cowin site "
                    for each_mail in email_list:
                        s.sendmail("EMAILID@gmail.com", each_mail, message)
                    s.quit()

                    flag = False
