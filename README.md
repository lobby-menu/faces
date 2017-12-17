# Faces
Faces is the face recognition part of the Lobby Backend project. It's aim is to create a dynamic database of customers that frequent the restaurant. Making it possible to id the customers nothing but their faces.

It accepts a photo of a customer, and returns the possible matches with a percentage score of the match. Then you can either let the service automatically create a relation with the face you sent and some result in the database, or you can make it so you will have to manually mark the relationship between faces with a second REST api call.

## Design Principles
The aim is to create a database of faces and a somewhat correct clustering of these faces. Face ids and clustering(person) ids will be unique identifiers that will be used to associate metadata with a single person.

This clustering of faces maybe reversible, in case we find a better algorithm.

## REST API Methods
Below are the methods which can be accessed via HTTP.

### POST /faces/create
Detects and aligns a face in the given image. Giving it an id. This will make sure that the image you have has a valid face in it.

In case of multiple faces, calculates a score according to the distance of each face to the center, and their size, picks the highest scored one and creates a face id for it.

### GET /faces/{id}
Returns metadata about the face like its create date, and images of its aligned and original states. Returns the relation of the face to a person if there is any.

### POST /faces/identify
Groups the given faces into what it thinks are different persons, and returns a list of top persons it thinks each groups belong to.

### POST /faces/relation
For a list of faces, creates a relation to a specific person.

### GET /person/{id}
For a given user, return the related face ids, and metadata information about the faces.
