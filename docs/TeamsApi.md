# swagger_client.TeamsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**count_of_teams_counts_teams_v1_get**](TeamsApi.md#count_of_teams_counts_teams_v1_get) | **GET** /counts/teams/v1 | Count Of Teams
[**list_teams_platforms_platform_teams_v1_get**](TeamsApi.md#list_teams_platforms_platform_teams_v1_get) | **GET** /platforms/{platform}/teams/v1 | List Teams
[**list_teams_teams_v1_get**](TeamsApi.md#list_teams_teams_v1_get) | **GET** /teams/v1 | List Teams
[**team_platforms_platform_teams_v1_identifier_get**](TeamsApi.md#team_platforms_platform_teams_v1_identifier_get) | **GET** /platforms/{platform}/teams/v1/{identifier} | Team
[**team_teams_v1_identifier_delete**](TeamsApi.md#team_teams_v1_identifier_delete) | **DELETE** /teams/v1/{identifier} | Team
[**team_teams_v1_identifier_get**](TeamsApi.md#team_teams_v1_identifier_get) | **GET** /teams/v1/{identifier} | Team
[**team_teams_v1_identifier_put**](TeamsApi.md#team_teams_v1_identifier_put) | **PUT** /teams/v1/{identifier} | Team
[**team_teams_v1_post**](TeamsApi.md#team_teams_v1_post) | **POST** /teams/v1 | Team

# **count_of_teams_counts_teams_v1_get**
> object count_of_teams_counts_teams_v1_get()

Count Of Teams

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.TeamsApi()

try:
    # Count Of Teams
    api_response = api_instance.count_of_teams_counts_teams_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TeamsApi->count_of_teams_counts_teams_v1_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_teams_platforms_platform_teams_v1_get**
> object list_teams_platforms_platform_teams_v1_get(platform, schema=schema, offset=offset, limit=limit)

List Teams

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.TeamsApi()
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Teams
    api_response = api_instance.list_teams_platforms_platform_teams_v1_get(platform, schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TeamsApi->list_teams_platforms_platform_teams_v1_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **platform** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]
 **offset** | [**object**](.md)|  | [optional] [default to 0]
 **limit** | [**object**](.md)|  | [optional] [default to 100]

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_teams_teams_v1_get**
> object list_teams_teams_v1_get(schema=schema, offset=offset, limit=limit)

List Teams

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.TeamsApi()
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Teams
    api_response = api_instance.list_teams_teams_v1_get(schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TeamsApi->list_teams_teams_v1_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **schema** | [**object**](.md)|  | [optional] [default to aiod]
 **offset** | [**object**](.md)|  | [optional] [default to 0]
 **limit** | [**object**](.md)|  | [optional] [default to 100]

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **team_platforms_platform_teams_v1_identifier_get**
> TeamRead team_platforms_platform_teams_v1_identifier_get(identifier, platform, schema=schema)

Team

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.TeamsApi()
identifier = NULL # object | 
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Team
    api_response = api_instance.team_platforms_platform_teams_v1_identifier_get(identifier, platform, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TeamsApi->team_platforms_platform_teams_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **platform** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**TeamRead**](TeamRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **team_teams_v1_identifier_delete**
> object team_teams_v1_identifier_delete(identifier)

Team

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.TeamsApi(swagger_client.ApiClient(configuration))
identifier = NULL # object | 

try:
    # Team
    api_response = api_instance.team_teams_v1_identifier_delete(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TeamsApi->team_teams_v1_identifier_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **team_teams_v1_identifier_get**
> TeamRead team_teams_v1_identifier_get(identifier, schema=schema)

Team

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.TeamsApi()
identifier = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Team
    api_response = api_instance.team_teams_v1_identifier_get(identifier, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TeamsApi->team_teams_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**TeamRead**](TeamRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **team_teams_v1_identifier_put**
> object team_teams_v1_identifier_put(body, identifier)

Team

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.TeamsApi(swagger_client.ApiClient(configuration))
body = swagger_client.TeamCreate() # TeamCreate | 
identifier = NULL # object | 

try:
    # Team
    api_response = api_instance.team_teams_v1_identifier_put(body, identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TeamsApi->team_teams_v1_identifier_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TeamCreate**](TeamCreate.md)|  | 
 **identifier** | [**object**](.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **team_teams_v1_post**
> object team_teams_v1_post(body)

Team

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.TeamsApi(swagger_client.ApiClient(configuration))
body = swagger_client.TeamCreate() # TeamCreate | 

try:
    # Team
    api_response = api_instance.team_teams_v1_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TeamsApi->team_teams_v1_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TeamCreate**](TeamCreate.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

