from django.contrib import admin
from django.shortcuts import render
from .models import *
from django.urls import path
from django import forms
import datetime
# from datetime import datetime
import re
import time
import asyncio



# This form will be rendered using the 'upload_csv' function whose objective is to render the "csv_upload.html" file.
class CSVImportForm(forms.Form):
    csv_upload = forms.FileField()



# Build an asynchronous function to insert all the trade-logs into the DB
def insertLog(date_f, field1, field2, field3, field4, field5, field6):
    # create each record inside the DB while iterating
    # try:
    created = TradeLog.objects.update_or_create(
        date = date_f,
        trade_code = field1,
        high = float(field2),
        low = float(field3),
        open = float(field4),
        close = float(field5),
        volume = int(field6),
    )
    # there are some empty value inside the "Volume" column
    # except ValueError:
    #     pass



i = 0


class TradeLogAdmin(admin.ModelAdmin):
    list_display = ['date', 'trade_code', 'high', 'low', 'open', 'close', 'volume']

    # the controller of "upload_csv" function is appended here along with other existing URLs of this django-proj
    def get_urls(self):
        # Get all the exisiting URLs of this Dj proj
        urls = super().get_urls()
        new_urls = [
            path('upload_csv/', self.upload_csv),
        ]
        print(urls)
        return new_urls + urls

    # this function is responsible for rendering the admin to the csv_uploading page, Also insert the CSV files data into the database.
    def upload_csv(self, request):
        if request.method == 'POST':
            # print('action is post!')

            # [ IMPORTANT ]: The CSV file should not contain any table column-titles

            # Get the csv_file from the form
            csv_file = request.FILES['csv_upload']

            # read the data inside of the CSV_file
            file_data = csv_file.read().decode("utf-8")
            # split the data on the new-line ("\n") and convert each data into a list. This list will contain each record of name & balance
            csv_data = file_data.split('\n')

            # print(type(csv_data))
            # rmeote the coulumn heading from dataset
            csv_data = csv_data[1:]
            # print(csv_data)
            # print(len(csv_data))
            # print('\n'*3)

            # u = 0
            for i in range(len(csv_data)):
                # print(csv_data[i])

                x = csv_data[i]

                # ------------ Get all the values from the 'Volumes' column from the long-string of csv
                # "get a value inside double-quotation from string using python regex"
                # Ref:  https://stackoverflow.com/a/9519934
                matches = re.findall(r'"(.+?)"',x)
                # matches is now ['String 1', 'String 2', 'String3']
                xx = ",".join(matches)

                xx=xx.replace(',',"")
                # print(xx)

                fields = x.split(",")

                # print(fields)

                # print(fields[1])

                
                # try:
                    # print(fields[0])
                #     # print(fields[1])
                #     # print(fields[2])
                #     # print(fields[3])
                #     # print(fields[4])
                #     # print(fields[5])
                #     print(xx)
                #     time.sleep(0.001)
                    # print(fields[0], '----', fields[1],fields[2], '----', fields[3],fields[4], '----', fields[5], '----', xx, '----', i)
                #     # u += 1
                # except:
                #     pass

            #     # if fields[0] != IndexError:
            #     #     print(fields[0], '----', fields[1])

            #     # print(fields[0], '----', fields[1],fields[2], '----', fields[3],fields[4], '----', fields[5],fields[6], '----', xx)


            # print(u)
            # for x in csv_data:
            #     # print(dir(x))

            #     # ------------ Get all the values from the 'Volumes' column from the long-string of csv
            #     # "get a value inside double-quotation from string using python regex"
            #     # Ref:  https://stackoverflow.com/a/9519934
            #     matches = re.findall(r'"(.+?)"',x)
            #     # matches is now ['String 1', 'String 2', 'String3']
            #     xx = ",".join(matches)


            #     # "remove all the commas from the 'Volume' integer"
            #     # Ref: https://java2blog.com/remove-comma-from-string-python/#:~:text=You%20can%20remove%20comma%20from,using%20string's%20replace()%20method.
            #     xx=xx.replace(',',"")
            #     # print(xx)
            #     # # ------------



            #     # Now split each elem of the parent list before actually inserting each record in the specific DB table
            #     fields = x.split(",")
            #     # print(fields)
            #     # print(fields[:-1])
            #     print(fields[0], '----', fields[1],fields[2], '----', fields[3],fields[4], '----', fields[5],fields[6], '----', xx)

                # print((fields[0]))    # [Output-date]: 2020-08-10,2020-07-29,2020-07-14,.....
                # print((fields[1]))    # [Output-trade_code]: 1JANATAMF,1JANATAMF,.....
            #     # print(type(float(fields[2])))     # [Output-high]: 4.3,4.9.6.3,.....
            #     # print(float(fields[3]))     # [Output-low]: 4.3,4.3.4.3,.....
            #     # print(float(fields[4]))     # [Output-open]: 4.1,4.1.4.1,.....
            #     # print(float(fields[5]))     # [Output-close]: 4.2,4.2.4.2,.....
            #     # print(float(fields[6]))     # [Output-volume]: 4.2,4.2.4.2,.....


            #     # convert the date string into the python's datetime format which is accepted in the database
                # date_split = fields[0].split('-')
                # print(date_slipt[0])    # year
                # print(date_slipt[1])  # month
                # time.sleep(0.005)
                # print(date_slipt[2])  # day
                # year,month,day = fields[0].split('-')
                date_split = fields[0].split('-')
                if len(date_split) != 1:
                    # print(date_split)

                    # [Add multiple values from a list into multiple variables at the same time]
                    # Ref:   https://careerkarma.com/blog/python-valueerror-built-in-function-or-method-is-not-iterable/
                    year,month,day = date_split
                # print(year,'-',month,'-',day)
                # year = date_slipt[0]    # int(date_slipt[0])
                # month = date_slipt[1]   # int(date_slipt[1])
                # day = date_slipt[2]     # int(date_slipt[2])
                # date_formated = datetime.date(year,month,day)
                    date_formated = datetime.date(int(year),int(month),int(day))
                # date_formated = datetime.date(int(date_split[0]),int(date_split[1]),int(date_split[2]))
                # i+=1
                # print(date_formated, '----', f'{i}')
                # print(date_formated)


                # date_formated = f'{date_slipt[0]}/{date_slipt[1]}/{date_slipt[3]}'
                # date_obj = datetime.strptime(date_formated, '%d/%m/%y %H:%M:%S')
                # print(date_obj)

                insertLog(
                    date_formated,
                    fields[1], 
                    fields[2], 
                    fields[3], 
                    fields[4], 
                    fields[5], 
                    xx, 
                )


                # call the 'insertLog' fucntion to inser data into the DB
                # try:
                    # insertLog(
                    #     date_formated=date_formated,
                    #     field1=fields[1], 
                    #     field2=fields[2], 
                    #     field3=fields[3], 
                    #     field4=fields[4], 
                    #     field5=fields[5], 
                    #     field6=fields[6], 
                    # )
                # except IndexError:
                #     pass

                # # create each record inside the DB while iterating
                # try:
                    # created = TradeLog.objects.update_or_create(
                    #     date = date_formated,
                    #     trade_code = fields[1],
                    #     high = float(fields[2]),
                    #     low = float(fields[3]),
                    #     open = float(fields[4]),
                    #     close = float(fields[5]),
                    #     volume = int(xx),
                    # )
                # # there are some empty value inside the "Volume" column
                # except ValueError:
                #     pass
            #     pass
            

        # render the empty django-form to upload CSV file.
        form = CSVImportForm()
        context = {
            'form': form
        }

        return render(request, 'admin/csv_upload.html', context)

admin.site.register(TradeLog, TradeLogAdmin)

