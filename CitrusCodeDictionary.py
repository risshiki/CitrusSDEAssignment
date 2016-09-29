import csv
import string

import random
import sys
import time

start_time = time.time()

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def convert_records(inputfile, outputfile):
    phone_dict = {}
    email_dict = {}
    uniqueid_dict = {}
    final_dict = {}

    flag1 = False
    flag2 = False

    try:
        f = open(inputfile,'rt')

        #string = f.readlines()

        reader = csv.reader(f)
        next(reader)                #Ignoring the header descriptions

        counter = 0
        for row in reader:
            
            email_id = row[0].rstrip()
            phone_number = row[1].rstrip()
            len_e = len(email_id)
            len_p = len(phone_number)
            flag1 = False
            flag2 = False

            

            
            if email_id not in email_dict and phone_number not in phone_dict:
                uid = id_generator().rstrip()
                
                # Takes care of the cases where only a unique email is added
                if len_e > 5 and email_id != '\\Z':    
                    email_dict[email_id] = uid
                    flag1 = True
                # Takes care of the cases where only a unique phone number is added

                if len_p > 8 and phone_number!='\\Z':    
                    phone_dict[phone_number] = uid
                    flag2 = True
                    
                if uid not in uniqueid_dict.keys():                                             # To take care of duplicate entries
                    uniqueid_dict[uid] = None
                    
                    if flag1 == True and flag2 == True:
                         final_dict[uid] = [email_id, phone_number]

                    elif flag1 and not flag2:
                        final_dict[uid] = [email_id]
                    elif not flag1 and flag2:
                        final_dict[uid] = [phone_number]
                    
                    
            elif email_id in email_dict and phone_number not in phone_dict:
                


                if '\\Z' not in phone_number and len_p > 8:
                    uid = email_dict[email_id]
                    phone_dict[phone_number] = uid
                    final_dict[uid].append(phone_number)
                    

            elif email_id not in email_dict and phone_number in phone_dict:
                

                if '\\Z' not in email_id and len_e > 5:
                    uid = phone_dict[phone_number]
                    email_dict[email_id] = uid
                    final_dict[uid].append(email_id)


            elif email_id in email_dict and phone_number in phone_dict:         # Very unique case where two previously generated id's need to be consolidated into one

                ph_uid = phone_dict[phone_number]
                e_uid = email_dict[email_id]

                if ph_uid != e_uid:    
                    for element in final_dict[e_uid]:
                        final_dict[ph_uid].append(element)
                    
                    email_dict[email_id] = ph_uid
                    del final_dict[e_uid]

        f.close()            
    except IOError:
        print('cannot open', inputfile)
        
    


    r = open(outputfile,'wt',newline = '')

    try:
        writer = csv.writer(r)
        writer.writerow(('Unique ID', 'List of Attributes'))
        for key, value in final_dict.items():
            writer.writerow((key,value))
        r.close()
        
    except IOError:
        print('cannot open', outputfile)
        
        
        

convert_records("casestudy.csv","output.csv")

print("%s seconds" % (time.time() - start_time))

