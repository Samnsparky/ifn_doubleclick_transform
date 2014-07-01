IFN DoubleClick Transform Tool
==============================
The DoubleClick codes and targeting might need to change in the future for IFN Occam content. This tool allows many of those DoubleClick codes to be updated in bulk. However, note that, while this tool was intended to update DoubleClick information, this utility may also be used to update any other properties of content and channels with some modification.

<br>
Writing Transformation JSON Files
---------------------------------
The JSON document must contain a root object with a ```transformations``` attribute. That required attribute should have an array of objects as its value. The objects within that array are called rules. Every rule must have a ```starts_with``` attribute that describes what the slug of the articles / channels must be in order to be transformed by this rule. The other attributes of the rule will be written to the matching channels / articles. See test_transform.json for an example!

<br>
Running the tool
----------------
Make sure you have pymongo installed with ```pip install pymongo```. Then, invoke the tool from the command line:

```python ifn_doubleclick_transform.py [URI] [DB] [JSON]```

 - ```URI```: The full MongoDB URI where the target database can be accessed. This does not need to include the database name but it may.
 - ```DB```: The name of the databaes to operate on. This will use the users collection within that database. This argument but be specified regardless of if it is in the URI.
 - ```JSON```: Path to the JSON file with information on the transformations to execute.

For example, ```python ifn_doubleclick_transform.py mongodb://localhost ifn ./test_transform.json``` would execute the tool on the ifn database within the mongo instance running on the local machine using the rules defined in test_transform.json.
