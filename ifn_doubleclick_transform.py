"""Convenience command line utility to change double click preferences in mass.
 
Convenience command line utility that changes the DoubleClick prefences in
mass for both articles and channels within the CMS. Note that this does affect
the resource directory which has its own ads overwritting mechanism.
 
@author: Sam Pottinger (Gleap LLC, 2014)
@license: GNU GPL v3
"""

import json
import sys


# Help text and information about arguments required
NUM_ARGS = 3
USAGE_STR = '''USAGE: python ifn_doubleclick_transform.py [URI] [DB] [JSON]
 
Changes the DoubleClick prefences in mass for both articles and channels within
the CMS. Note that this does affect the resource directory which has its own ads
overwritting mechanism. Transforms are done according to the provided JSON file.
 
URI: The full MongoDB URI where the target database can be accessed. This does 
     not need to include the database name but it may.
 
DB: The name of the databaes to operate on. This will use the users
    collection within that database. This argument but be specified
    regardless of if it is in the URI.
 
JSON: Path to the JSON file with information on the transformations to execute.
'''


imports_successful = False
try:
    import pymongo
    imports_successful = True
except:
    print 'Whoops! You don\'t have pymongo... Try pip install pymongo.'


def execute_channel_transform(transformation, db_client):
    """Update the DoubleClick configuration for matching channels.

    Update the DoubleClick configuration for channels according to the provided
    transformation as loaded from the JSON file.

    @param transformation: The transformation to execute as loaded from the
        JSON file.
    @type transformation: dict
    @param db_client: The database to execute the transformation on.
    @type db_client: pymongo.db
    """
    new_doc = {}
    for key in transformation:
        if key != 'starts_with':
            new_doc[key] = transformation[key]

    db_client.channel.update(
        {'slug': {'$regex': transformation['starts_with'] + '.*'}},
        {'$set': new_doc},
        multi=True
    )


def execute_content_transform(transformation, db_client):
    """Update the DoubleClick configuration for matching content.

    Update the DoubleClick configuration for articles according to the provided
    transformation as loaded from the JSON file.

    @param transformation: The transformation to execute as loaded from the
        JSON file.
    @type transformation: dict
    @param db_client: The database to execute the transformation on.
    @type db_client: pymongo.db
    """
    new_doc = {}
    for key in transformation:
        if key != 'starts_with':
            new_doc[key] = transformation[key]

    db_client.content.update(
        {'slug': {'$regex': transformation['starts_with'] + '.*'}},
        {'$set': new_doc},
        multi=True
    )


def main(mongo_uri, db_name, json_path):
    """Main program logic that executes transforms.

    Main script logic that reads the JSON instructions from json_path and
    executes those operations on the database at mongo_uri.

    @param mongo_uri: The URI of the mongo instance to operate on.
    @type mongo_uri: str
    @param db_name: The name of the database to operate on at the instance
        running at mongo_uri.
    @type db_name: str
    @param json_path: The path to the JSON file with transformation information.
    @type json_path: str
    """
    db_client = pymongo.MongoClient(mongo_uri)[db_name]

    with open(json_path) as f:
        transforms = json.load(f)['transformations']

    for transformation in transforms:
        execute_content_transform(transformation, db_client)
        execute_channel_transform(transformation, db_client)

    print '[ SUCCESS ]'


if __name__ == '__main__':
    if imports_successful:
        if len(sys.argv) < NUM_ARGS + 1: 
            print USAGE_STR
        else:
            main(sys.argv[1], sys.argv[2], sys.argv[3])
