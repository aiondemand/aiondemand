# swagger_client.PersonsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**count_of_persons_counts_persons_v1_get**](PersonsApi.md#count_of_persons_counts_persons_v1_get) | **GET** /counts/persons/v1 | Count Of Persons
[**list_persons_persons_v1_get**](PersonsApi.md#list_persons_persons_v1_get) | **GET** /persons/v1 | List Persons
[**list_persons_platforms_platform_persons_v1_get**](PersonsApi.md#list_persons_platforms_platform_persons_v1_get) | **GET** /platforms/{platform}/persons/v1 | List Persons
[**person_persons_v1_identifier_delete**](PersonsApi.md#person_persons_v1_identifier_delete) | **DELETE** /persons/v1/{identifier} | Person
[**person_persons_v1_identifier_get**](PersonsApi.md#person_persons_v1_identifier_get) | **GET** /persons/v1/{identifier} | Person
[**person_persons_v1_identifier_put**](PersonsApi.md#person_persons_v1_identifier_put) | **PUT** /persons/v1/{identifier} | Person
[**person_persons_v1_post**](PersonsApi.md#person_persons_v1_post) | **POST** /persons/v1 | Person
[**person_platforms_platform_persons_v1_identifier_get**](PersonsApi.md#person_platforms_platform_persons_v1_identifier_get) | **GET** /platforms/{platform}/persons/v1/{identifier} | Person

# **count_of_persons_counts_persons_v1_get**
> object count_of_persons_counts_persons_v1_get()

Count Of Persons

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PersonsApi()

try:
    # Count Of Persons
    api_response = api_instance.count_of_persons_counts_persons_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PersonsApi->count_of_persons_counts_persons_v1_get: %s\n" % e)
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

# **list_persons_persons_v1_get**
> object list_persons_persons_v1_get(schema=schema, offset=offset, limit=limit)

List Persons

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PersonsApi()
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Persons
    api_response = api_instance.list_persons_persons_v1_get(schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PersonsApi->list_persons_persons_v1_get: %s\n" % e)
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

# **list_persons_platforms_platform_persons_v1_get**
> object list_persons_platforms_platform_persons_v1_get(platform, schema=schema, offset=offset, limit=limit)

List Persons

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PersonsApi()
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Persons
    api_response = api_instance.list_persons_platforms_platform_persons_v1_get(platform, schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PersonsApi->list_persons_platforms_platform_persons_v1_get: %s\n" % e)
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

# **person_persons_v1_identifier_delete**
> object person_persons_v1_identifier_delete(identifier)

Person

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.PersonsApi(swagger_client.ApiClient(configuration))
identifier = NULL # object | 

try:
    # Person
    api_response = api_instance.person_persons_v1_identifier_delete(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PersonsApi->person_persons_v1_identifier_delete: %s\n" % e)
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

# **person_persons_v1_identifier_get**
> PersonRead person_persons_v1_identifier_get(identifier, schema=schema)

Person

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PersonsApi()
identifier = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Person
    api_response = api_instance.person_persons_v1_identifier_get(identifier, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PersonsApi->person_persons_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**PersonRead**](PersonRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **person_persons_v1_identifier_put**
> object person_persons_v1_identifier_put(body, identifier)

Person

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.PersonsApi(swagger_client.ApiClient(configuration))
body = swagger_client.PersonCreate() # PersonCreate | 
identifier = NULL # object | 

try:
    # Person
    api_response = api_instance.person_persons_v1_identifier_put(body, identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PersonsApi->person_persons_v1_identifier_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PersonCreate**](PersonCreate.md)|  | 
 **identifier** | [**object**](.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **person_persons_v1_post**
> object person_persons_v1_post(body)

Person

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.PersonsApi(swagger_client.ApiClient(configuration))
body = swagger_client.PersonCreate() # PersonCreate | 

try:
    # Person
    api_response = api_instance.person_persons_v1_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PersonsApi->person_persons_v1_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PersonCreate**](PersonCreate.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **person_platforms_platform_persons_v1_identifier_get**
> PersonRead person_platforms_platform_persons_v1_identifier_get(identifier, platform, schema=schema)

Person

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PersonsApi()
identifier = NULL # object | 
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Person
    api_response = api_instance.person_platforms_platform_persons_v1_identifier_get(identifier, platform, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PersonsApi->person_platforms_platform_persons_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **platform** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**PersonRead**](PersonRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

