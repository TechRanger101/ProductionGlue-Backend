import json
from pinecone import Pinecone
import time
import uuid
import pandas as pd
import numpy as np
from config import *
from db import *
from map import *
from decimal import Decimal
from openai import OpenAI
from datetime import datetime


pc = Pinecone(api_key=PINECONE_API_KEY)
pindex = pc.Index(PINECONE_INDEX)

client = OpenAI(api_key=OPENAI_API_KEY)

def get_embedding(text):
    response = client.embeddings.create(input=text, model=EMBEDDING_MODEL)
    return response.data[0].embedding

def preprocess_venue_data(file_path):
    df = pd.read_csv(file_path)
    # Replace np.inf, -np.inf with None to handle infinities and use pd.isna to find NaNs
    df = df.replace([np.inf, -np.inf], None)
    # Replace NaN with None
    df = df.where(~pd.isna(df), None)
    items = df.to_dict(orient='records')

    zip_to_lat_lng = {}
    new_items = []
    for item in items:
        item['eventEntityId'] = str(uuid.uuid4()).replace("-", "") + str(int(time.time()*1000))
        # Convert all float values to Decimals, skip over None, NaN and Inf values
        for k, v in item.items():
            if isinstance(v, float):
                if v is not None and not np.isnan(v) and not np.isinf(v):
                    item[k] = Decimal(str(v))
                else:
                    item[k] = None
            else:
                item[k] = v
        item['read_status'] = 'new'
        item['type'] = 'venue'
        item['rating'] = '5'
        item['createdBy'] = 'admin'
        item['category'] = 'Default'
        try:
            if zip_to_lat_lng.get(item['zipCode']) is not None:
                lat_lang = zip_to_lat_lng.get(item['zipCode'])
            else:
                lat_lang = get_lat_lng_for_zip(item['zipCode'])
                zip_to_lat_lng[item['zipCode']] = lat_lang
            print(lat_lang)
            item['lat'], item['lng'] = Decimal(str(lat_lang[0])), Decimal(str(lat_lang[1]))
            new_items.append(item)
        except:
            pass
    return new_items

def preprocess_vendor_data(file_path):
    df = pd.read_excel(file_path)
    # Replace np.inf, -np.inf with None to handle infinities and use pd.isna to find NaNs
    df = df.replace([np.inf, -np.inf], None)
    # Replace NaN with None
    df = df.where(~pd.isna(df), None)
    df = df.replace({pd.NaT: None})
    items = df.to_dict(orient='records')

    zip_to_lat_lng = {}
    new_items = []
    for item in items:
        item['eventEntityId'] = str(uuid.uuid4()).replace("-", "") + str(int(time.time()*1000))
        # Convert all float values to Decimals, skip over None, NaN and Inf values
        for k, v in item.items():
            if isinstance(v, (pd.Timestamp, datetime)):
                item[k] = v.isoformat()
            elif isinstance(v, float):
                if v is not None and not np.isnan(v) and not np.isinf(v):
                    item[k] = Decimal(str(v))
                else:
                    item[k] = None
            else:
                item[k] = v
        item['read_status'] = 'new'
        item['type'] = 'vendor'
        item['rating'] = '5'
        item['createdBy'] = 'admin'
        try:
            if zip_to_lat_lng.get(item['zipCode']) is not None:
                lat_lang = zip_to_lat_lng.get(item['zipCode'])
            else:
                lat_lang = get_lat_lng_for_zip(item['zipCode'])
                zip_to_lat_lng[item['zipCode']] = lat_lang
            print(lat_lang)
            item['lat'], item['lng'] = Decimal(str(lat_lang[0])), Decimal(str(lat_lang[1]))
            new_items.append(item)
            # print(item)
        except:
            # print(item)
            pass
    return new_items

def import_data():
    # venue_items = preprocess_venue_data('data/venue_data.csv')
    vendor_items = preprocess_vendor_data('data/vendor_data.xlsx')
    add_batch_items('VenuesAndVendors', vendor_items)

def process_embedding_items(items):
    ids, new_items, embeddings = [], [], []
    for item in items:
        text = ""
        new_item = {}
        for k, v in item.items():
            if v is not None:
                text += f"{k}: {str(v)}\n"
                new_item[k] = str(v)
        ids.append(item['eventEntityId'])
        new_items.append(new_item)
        embeddings.append(get_embedding(text))
    return ids, new_items, embeddings
    
def build_knowledge_base():
    venue_items = query_items('vendor')
    rest = len(venue_items)%100 + 100
    for i in range(0, len(venue_items)-rest, 100):
        ids, new_items, embeddings = process_embedding_items(venue_items[i: i+100])
        print('finished embedding')
        records = zip(ids, embeddings, new_items)
        pindex.upsert(records)
    ids, new_items, embeddings = process_embedding_items(venue_items[len(venue_items)-rest+100:])
    print('finished embedding')
    records = zip(ids, embeddings, new_items)
    pindex.upsert(records)

def search_knowledge(query, top_k=10):
    query_vector = get_embedding(query)
    result = pindex.query(vector=query_vector, top_k=top_k)
    matches = result.to_dict()['matches']
    ids = [match['id'] for match in matches]
    data = pindex.fetch(ids).to_dict()['vectors']
    response = [data[id]['metadata'] for id in ids]
    print(len(response))
    return response

def search_knowledge_assistant(query, top_k=10):
    return json.dumps(search_knowledge(query, top_k))

def convert_Decimal_to_float(data_list):
    new_data_list = []
    for data in data_list:
        new_data = {}
        for key, value in data.items():
            if isinstance(value, Decimal):
                new_data[key] = float(value)
            elif value is not None:
                new_data[key] = value
        new_data_list.append(new_data)
    print(len(new_data))
    return json.dumps(new_data_list)

def miles_to_kilometers(miles):
    return miles * 1.60934

def filterData(data):
    new_places = []
    for place in data:
        p = {}
        for k, v in place.items():
            if v is not None:
                p[k] = v
        new_places.append(p)
    return new_places

def filterPlaces(search_type, service_type):
    places = place_data[search_type]
    if search_type == 'venue':
        serviceType_key = 'serviceType'
    else:
        serviceType_key = 'serviceCategory'
    filtered_places = []
    if service_type != "none":
        for p in places:
            try:
                if service_type.lower() in p[serviceType_key].lower():
                    filtered_places.append(p)
            except:
                pass
        print(len(filtered_places))
        return filtered_places
    else:
        return places

def online_search():
    pass

place_data = {
    'venue': filterData(query_items('venue')),
    'vendor': filterData(query_items('vendor'))
}
