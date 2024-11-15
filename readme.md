# Arches CIIM integration

Current version for 7.5.x

## APIs

### /resource/changes 
Used to get a json view of all resources and the latest changes
Called with the from and to dates, sort order, per page and page number
e.g. http://127.0.0.1:8000/resource/changes?from=01-01-2022T00:00:00Z&to=27-10-2027T00:00:00Z&sortField=id&sortOrder=asc&perPage=10&page=10

### /concept/export 
Used to get an xml output of all concepts 