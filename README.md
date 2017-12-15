# Faces
Faces is the face recognition part of the Lobby Backend project. It's aim is to create a dynamic database of customers that frequent the restaurant. Making it possible to id the customers nothing but their faces.

It accepts a photo of a customer, and returns the possible matches with a percentage score of the match. Then you can either let the service automatically create a relation with the face you sent and some result in the database, or you can make it so you will have to manually mark the relationship between faces with a second REST api call.

## REST API Methods
Below are the methods which can be accessed via HTTP.

### POST /faces/create
Detects and aligns a face in the given image. Giving it an id. This will make sure that the image you have has a valid face in it.

In case of multiple faces, calculates a score according to the distance of each face to the center, and their size, picks the highest scored one and creates a face id for it.

### GET /faces/{id}
Returns metadata about the face like its create date, and images of its aligned and original states.

### GET /faces/{id}/similar
Returns the similar faces for the given face.

### POST /faces/{id}/relation
Creates a relation to a person, given a face. In case no person is given, creates a new person.

### POST /faces/identify
This is a shorthand for `POST /faces/create` and `/faces/{id}/similar` with an option to also create a relation according to a given treshold by calling `POST /faces/{id}/relation`.


### GET /person/{id}
For a given user, return the related face ids, and metadata information about the faces.
