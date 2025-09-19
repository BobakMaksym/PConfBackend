from enums import Collection, Operation


pipeline = [
    {
        "$match": {
            "operationType": {"$in": Operation.values()},
            "ns.coll": {"$in": Collection.values()},
        }
    }
]
