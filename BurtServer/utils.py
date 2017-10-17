from wit import Wit
import requests

access_token = "OF4G7O5U4MBAQU5GMSZUOUIHBMLYD4QV"

client = Wit(access_token = access_token)

def wit_response(message_text):
    resp = client.message(message_text)
    entity = None
    value = None

    try:
        entities = list(resp['entities'])
        values = []
        for entity in entities:
            values.append(resp['entities'][entity][0]['value'])
    except:
        pass
    return(entities, values)

"""
entities, values = wit_response("thanks")
print "entities: %s " % entities        #DEBUG
print "values: %s " % values            #DEBUG
"""