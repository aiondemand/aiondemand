# swagger_client.PlatformsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**count_of_platforms_counts_platforms_v1_get**](PlatformsApi.md#count_of_platforms_counts_platforms_v1_get) | **GET** /counts/platforms/v1 | Count Of Platforms
[**list_platforms_platforms_v1_get**](PlatformsApi.md#list_platforms_platforms_v1_get) | **GET** /platforms/v1 | List Platforms
[**platform_platforms_v1_identifier_delete**](PlatformsApi.md#platform_platforms_v1_identifier_delete) | **DELETE** /platforms/v1/{identifier} | Platform
[**platform_platforms_v1_identifier_get**](PlatformsApi.md#platform_platforms_v1_identifier_get) | **GET** /platforms/v1/{identifier} | Platform
[**platform_platforms_v1_identifier_put**](PlatformsApi.md#platform_platforms_v1_identifier_put) | **PUT** /platforms/v1/{identifier} | Platform
[**platform_platforms_v1_post**](PlatformsApi.md#platform_platforms_v1_post) | **POST** /platforms/v1 | Platform

# **count_of_platforms_counts_platforms_v1_get**
> object count_of_platforms_counts_platforms_v1_get()

Count Of Platforms

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PlatformsApi()

try:
    # Count Of Platforms
    api_response = api_instance.count_of_platforms_counts_platforms_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PlatformsApi->count_of_platforms_counts_platforms_v1_get: %s\n" % e)
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

# **list_platforms_platforms_v1_get**
> object list_platforms_platforms_v1_get(schema=schema, offset=offset, limit=limit)

List Platforms

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PlatformsApi()
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Platforms
    api_response = api_instance.list_platforms_platforms_v1_get(schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PlatformsApi->list_platforms_platforms_v1_get: %s\n" % e)
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

# **platform_platforms_v1_identifier_delete**
> object platform_platforms_v1_identifier_delete(identifier)

Platform

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.PlatformsApi(swagger_client.ApiClient(configuration))
identifier = NULL # object | 

try:
    # Platform
    api_response = api_instance.platform_platforms_v1_identifier_delete(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PlatformsApi->platform_platforms_v1_identifier_delete: %s\n" % e)
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

# **platform_platforms_v1_identifier_get**
> PlatformRead platform_platforms_v1_identifier_get(identifier, schema=schema)

Platform

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PlatformsApi()
identifier = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Platform
    api_response = api_instance.platform_platforms_v1_identifier_get(identifier, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PlatformsApi->platform_platforms_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**PlatformRead**](PlatformRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **platform_platforms_v1_identifier_put**
> object platform_platforms_v1_identifier_put(body, identifier)

Platform

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.PlatformsApi(swagger_client.ApiClient(configuration))
body = swagger_client.PlatformCreate() # PlatformCreate | 
identifier = NULL # object | 

try:
    # Platform
    api_response = api_instance.platform_platforms_v1_identifier_put(body, identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PlatformsApi->platform_platforms_v1_identifier_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PlatformCreate**](PlatformCreate.md)|  | 
 **identifier** | [**object**](.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **platform_platforms_v1_post**
> object platform_platforms_v1_post(body)

Platform

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.PlatformsApi(swagger_client.ApiClient(configuration))
body = swagger_client.PlatformCreate() # PlatformCreate | 

try:
    # Platform
    api_response = api_instance.platform_platforms_v1_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PlatformsApi->platform_platforms_v1_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PlatformCreate**](PlatformCreate.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

