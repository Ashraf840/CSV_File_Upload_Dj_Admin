from django.contrib import admin
from django.shortcuts import render
from .models import *
from django.urls import path
from django import forms
import datetime
import re

from django.utils import timezone


# This form will be rendered using the 'upload_csv' function whose objective is to render the "csv_upload.html" file.
class CSVImportForm(forms.Form):
    csv_upload = forms.FileField()





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

    # this function is responsible for rendering the admin to the csv_uploading page, Also insert the (large) CSV files into the database.
    def upload_csv(self, request):
        if request.method == 'POST':
            start_time = timezone.now()
            csv_file = request.FILES['csv_upload']
            file_data = csv_file.read().decode("utf-8")
            # df = pd.read_csv(csv_file, sep='joursep', header=0)  
            csv_data = file_data.split('\n')
            csv_data = csv_data[1:-1]

            tradeLogData = []
            for i in range(len(csv_data)):
                # print(data)
                
                # ---------- Build the logic to insert bulk dataset into the DB ----------
                # print(csv_data[i])

                x = csv_data[i]

                # ------------ Get all the values from the 'Volumes' column from the long-string of csv
                # "get a value inside double-quotation from string using python regex"
                # Ref:  https://stackoverflow.com/a/9519934
                matches = re.findall(r'"(.+?)"', x)
                # matches is now ['String 1', 'String 2', 'String3']
                xx = ",".join(matches)

                xx = xx.replace(',', "")
                # print(xx)   # columes without commas, in 'string' format

                # split each
                fields = x.split(",")
                date_split = fields[0].split('-')

                year, month, day = date_split
                date_formated = datetime.date(int(year), int(month), int(day))
                # print(date_formated)  # col-1: date
                # print(fields[1])        # col-2: trade_code
                # print(fields[2])        # col-3: high
                # print(fields[3])        # col-4: low
                # print(fields[4])        # col-5: open
                # print(fields[5])        # col-6: close
                # print(int(xx))          # col-7: volume
                # time.sleep(0.001)

                try:
                    tdl = TradeLog(
                        date=date_formated,
                        trade_code=fields[1],
                        high=float(fields[2]),
                        low=float(fields[3]),
                        open=float(fields[4]),
                        close=float(fields[5]),
                        volume=int(xx),
                    )
                except ValueError:
                    tdl = TradeLog(
                        date=date_formated,
                        trade_code=fields[1],
                        high=0,
                        low=0,
                        open=0,
                        close=0,
                        volume=0,
                    )


                tradeLogData.append(tdl)

            # print(tradeLogData)

            
            
            # [ IMPORATNT NOTE ]
            # Ref:  https://betterprogramming.pub/3-techniques-for-importing-large-csv-files-into-a-django-app-2b6e5e47dba0

            # The main concept is to insert the bulk data (inside of a list-variable using the "bulk_create" queryset. Do Not Save One Element at a Time into the Database).
            # If we use the "TradeLog.objects.create(...)" query inside the for loop, then we are asking our database to commit the changes in each loop. 
            # Such I/O operations are very costly. Since this create-record query is pretty fast, there can be millions of such operations which can take 
            # use tremendous computational resources of the server, thus such I/O operations sould be avoided by using the "bulk_create()" queryset.

            # --------------------
            # [ NB ]: In order to delete a large amount of data from the DB, instead of using the GUI, execute the following dj-queryset to delete big amout of data from the DB thorugh dj-shell.
            # >>>> from appName.models import ClassModel
            # >>>> ClassModel.objects.all().delete()
            # --------------------

            TradeLog.objects.bulk_create(tradeLogData)
            end_time = timezone.now()

            # prints out the data insertion into the DB execution time,
            print(f"Loading CSV took: {(end_time-start_time).total_seconds()} seconds.")

        # render the empty django-form to upload CSV file.
        form = CSVImportForm()
        context = {
            'form': form
        }

        return render(request, 'admin/csv_upload.html', context)



admin.site.register(TradeLog, TradeLogAdmin)
