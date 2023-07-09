from django.db import connection
import csv
from io import StringIO
from django.db import models

def parse_file(csv_upload):
    data = []
    file = csv_upload.read().decode('utf-8')
    csv_data = csv.reader(StringIO(file), delimiter=',')
    for row in csv_data:
        data.append(row)
    return data

def install(model):
    with connection.schema_editor() as schema_editor:
        in_atomic_block = schema_editor.connection.in_atomic_block
        schema_editor.connection.in_atomic_block = False
        try:
            schema_editor.create_model(model)
        finally:
            schema_editor.connection.in_atomic_block = in_atomic_block


def create_new_model(csv_data, instance):

    attrs = {
        '__module__': 'api.models'
    }

    for row in csv_data[1:]:
        # print(row)
        # print()

        if row[3] == 'TRUE':
            mandatory = True
        elif row[3] == 'FALSE':
            mandatory = False
        else:
            continue

        if row[1] == 'text':
            if mandatory:
                attrs[row[0]] = models.CharField(max_length=1000, null=False, blank=False)
            else:
                attrs[row[0]] = models.CharField(max_length=1000, null=True, blank=True)

        elif row[1] == 'number':
            if mandatory:
                attrs[row[0]] = models.IntegerField(null=False, blank=False)
            else:
                attrs[row[0]] = models.IntegerField(null=True, blank=True)

        elif row[1] == 'date':
            if mandatory:
                attrs[row[0]] = models.DateField(null=False, blank=False)
            else:
                attrs[row[0]] = models.DateField(null=True, blank=True)

        elif row[1] == 'singleSelect':
            choices = row[2].split(',')
            if mandatory:
                attrs[row[0]] = models.TextField(null=False, blank=False, choices=choices)
            else:
                attrs[row[0]] = models.TextField(null=True, blank=True, choices=choices)
        

    new_model = type(instance.name, (models.Model,), attrs)
    
    return new_model
    