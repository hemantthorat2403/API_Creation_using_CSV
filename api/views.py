from .models import Form
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
import pymongo
import datetime

# server="localhost"
# port = 27017
# #Establish a connection with mongo instance.
client = MongoClient()
db = client['demo']


@api_view(['GET','POST'])
def get_post_api(request, form_name):
    coll_name = 'api_' + form_name
    dbtables = db.list_collection_names()
    
    if coll_name in dbtables:
    
        mycollection = db[coll_name]

        if request.method == 'GET':
            data = []
            cursor = mycollection.find({})
            for document in cursor:
                document.pop('_id')
                data.append(document)

            return Response(data, status=200)

        if request.method == 'POST':
            data = request.data
            res = {}
            form_obj = Form.objects.get(name=form_name)
            fields = form_obj.fields
            
            for field in fields:
                if field['mandatory']=='TRUE':
                    try:
                        data[field['field_name']]
                    except KeyError:
                        return Response({'message' : 'Enter all required field','response' : form_obj.error_resp}, status=400)


                try:
                    entry = data[field['field_name']]

                    if field['type']=='text':
                        if not isinstance(entry, str):
                            return Response({'message' : 'Data not valid','response' : form_obj.error_resp}, status=400)

                    if field['type']=='number':
                        if not isinstance(entry, int):
                            return Response({'message' : 'Data not valid','response' : form_obj.error_resp}, status=400)

                    if field['type']=='singleSelect':
                        if entry not in field['options'].split(','):
                            return Response({'message' : 'Data not valid','response' : form_obj.error_resp}, status=400)

                    if field['type']=='date':  
                        try:   
                            entry = datetime.datetime.strptime(f"{entry}", "%Y-%m-%d")
                        except ValueError:
                            return Response({'message' : 'Date not valid format=yyyy-mm-dd','response' : form_obj.error_resp}, status=400)

                    res[field['field_name']] = entry
                except KeyError:
                    if field['mandatory']=='FALSE':
                        continue
                    return Response({'message' : 'Data not valid','response' : form_obj.error_resp}, status=400)
                
            
            last_doc = mycollection.find_one(
                sort=[( '_id', pymongo.DESCENDING )]
            )

            if last_doc is None:
                last_doc = {}
                last_doc['id'] = 0
            
            res['id'] = last_doc['id']+1
            mycollection.insert_one(res)
            
            res.pop('_id')
            
            return Response(res, status=201)
    
    else:
        return Response({'Sorry.. No such form created.. Plz recheck url'}, status=404)


@api_view(['PUT','DELETE'])
def put_del_api(request, form_name, id):
    coll_name = 'api_' + form_name
    dbtables = db.list_collection_names()
    
    if coll_name in dbtables:
    
        mycollection = db[coll_name]

        res = mycollection.find_one({'id':id})
        if res is None:
            return Response({'message': 'No entry with this id'}, status=400)

        if request.method == 'DELETE':
            res.pop('_id')
            mycollection.delete_one({'id':id})
            res2 = {'message':'deleted successfully','obj':res}
            return Response(res2, status=200)

        if request.method == 'PUT':
            
            data = request.data
            data2 = {}
            form_obj = Form.objects.get(name=form_name)
            fields = form_obj.fields
            
            for field in fields:

                try:
                    entry = data[field['field_name']]

                    if field['type']=='text':
                        if not isinstance(entry, str):
                            return Response({'message' : 'Data not valid','response' : form_obj.error_resp}, status=400)

                    if field['type']=='number':
                        if not isinstance(entry, int):
                            return Response({'message' : 'Data not valid','response' : form_obj.error_resp}, status=400)

                    if field['type']=='singleSelect':
                        if entry not in field['options'].split(','):
                            return Response({'message' : 'Data not valid','response' : form_obj.error_resp}, status=400)

                    if field['type']=='date':  
                        try:   
                            entry = datetime.datetime.strptime(f"{entry}", "%Y-%m-%d")
                        except ValueError:
                            return Response({'message' : 'Date not valid format=yyyy-mm-dd','response' : form_obj.error_resp}, status=400)

                    data2[field['field_name']] = entry

                except KeyError:
                    if field['mandatory']=='FALSE':
                        continue
                    return Response({'message' : 'Data not valid','response' : form_obj.error_resp}, status=400)
                


            data2['id'] = id
            update_data = {'$set': data2}

            mycollection.update_one(res,update_data)

            return Response(data2, status=204)

    else:
        return Response({'Sorry.. No such form created.. Plz recheck url'}, status=404)