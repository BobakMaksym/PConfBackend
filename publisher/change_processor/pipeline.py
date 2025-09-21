from enums import Collection, Operation


pipeline = [
    {
        "$match": {
            "operationType": {"$in": Operation.values()},
            "ns.coll": {"$in": Collection.values()},
        }
    },
    {
        "$project": {"clusterTime": 0, "wallTime": 0},
    },
]
