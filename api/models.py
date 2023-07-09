from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from sqlalchemy import null
from .utils import parse_file, install, create_new_model


class Form(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    file = models.FileField()
    fields = models.JSONField(null=True, blank=True)
    error_resp = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


def addFields(csv_data, instance):
    data = []
    stdErrorResponse = {}
    for row in csv_data[1:]:
        data.append({
            'field_name':row[0],
            'type':row[1],
            'options':row[2],
            'mandatory':row[3]
        })

        if row[1]=='singleSelect':
            if row[3] == 'TRUE':
                stdErrorResponse[row[0]] = f'[{row[1]}] [{row[2]}] *required'
            else:
                stdErrorResponse[row[0]] = f'[{row[1]}] [{row[2]}] (optional)'
        else:
            if row[3] == 'TRUE':
                stdErrorResponse[row[0]] = f'[{row[1]}] *required'
            else:
                stdErrorResponse[row[0]] = f'[{row[1]}] (optional)'

    print(stdErrorResponse)
    instance.fields = data
    instance.error_resp = stdErrorResponse
    instance.save()


@receiver(post_save, sender=Form)
def createFormModel(sender, instance, created, **kwargs):
    if created:
        csv_data = parse_file(instance.file)
        new_model = create_new_model(csv_data, instance)
        install(new_model)
        addFields(csv_data, instance)

