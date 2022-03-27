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
from asgiref.sync import sync_to_async
import csv


# This form will be rendered using the 'upload_csv' function whose objective is to render the "csv_upload.html" file.
class CSVImportForm(forms.Form):
    csv_upload = forms.FileField()


# async def main(date_f, field1, field2, field3, field4, field5, field6):
#     task = asyncio.create_task(insertLog(date_f, field1, field2, field3, field4, field5, field6))
#     sync_to_async(task)


# Build an asynchronous function to insert all the trade-logs into the DB
def insertLog(date_f, field1, field2, field3, field4, field5, field6):
    # create each record inside the DB while iterating
    # try:

    TradeLog.objects.create(
        date=date_f,
        trade_code=field1,
        high=float(field2),
        low=float(field3),
        open=float(field4),
        close=float(field5),
        volume=int(field6),
    )
    # there are some empty value inside the "Volume" column
    # except ValueError:
    #     pass


class TradeLogAdmin(admin.ModelAdmin):
    list_display = ['date', 'trade_code',
                    'high', 'low', 'open', 'close', 'volume']

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
            # file_data = csv_file.read().decode("utf-8")
            file_data = csv.reader(csv_file, delimiter=",")
            # next(file_data)
            # split the data on the new-line ("\n") and convert each data into a list. This list will contain each record of name & balance
            csv_data = file_data.split('\n')

            # print(type(csv_data))
            # rmeote the coulumn heading from dataset
            # csv_data = csv_data[1:]
            # print(csv_data)
            # print(len(csv_data))
            # print('\n'*3)

            # print(len(csv_data))
            # print(csv_data[1])

            # # u = 0
            for i in range(len(csv_data)):
            # i = 1
            # while i < len(csv_data):
                print(csv_data[i])

                # x = csv_data[i]

                # # ------------ Get all the values from the 'Volumes' column from the long-string of csv
                # # "get a value inside double-quotation from string using python regex"
                # # Ref:  https://stackoverflow.com/a/9519934
                # matches = re.findall(r'"(.+?)"', x)
                # # matches is now ['String 1', 'String 2', 'String3']
                # xx = ",".join(matches)

                # xx = xx.replace(',', "")
                # # print(xx)

                # # split each
                # fields = x.split(",")
                # date_split = fields[0].split('-')
                # year, month, day = date_split
                # date_formated = datetime.date(int(year), int(month), int(day))
                # # print(date_formated)
                # # print(fields[5])
                # # print(xx)

                # # ------------- Requires a Message Broker -------------

                # # sync_to_async(insertLog(
                # #     date_formated,
                # #     fields[1],
                # #     fields[2],
                # #     fields[3],
                # #     fields[4],
                # #     fields[5],
                # #     xx,
                # # ))
                # # i += 1

        # render the empty django-form to upload CSV file.
        form = CSVImportForm()
        context = {
            'form': form
        }

        return render(request, 'admin/csv_upload.html', context)


admin.site.register(TradeLog, TradeLogAdmin)
