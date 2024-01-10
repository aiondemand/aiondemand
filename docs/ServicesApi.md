# swagger_client.ServicesApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**count_of_services_counts_services_v1_get**](ServicesApi.md#count_of_services_counts_services_v1_get) | **GET** /counts/services/v1 | Count Of Services
[**list_services_platforms_platform_services_v1_get**](ServicesApi.md#list_services_platforms_platform_services_v1_get) | **GET** /platforms/{platform}/services/v1 | List Services
[**list_services_services_v1_get**](ServicesApi.md#list_services_services_v1_get) | **GET** /services/v1 | List Services
[**service_platforms_platform_services_v1_identifier_get**](ServicesApi.md#service_platforms_platform_services_v1_identifier_get) | **GET** /platforms/{platform}/services/v1/{identifier} | Service
[**service_services_v1_identifier_delete**](ServicesApi.md#service_services_v1_identifier_delete) | **DELETE** /services/v1/{identifier} | Service
[**service_services_v1_identifier_get**](ServicesApi.md#service_services_v1_identifier_get) | **GET** /services/v1/{identifier} | Service
[**service_services_v1_identifier_put**](ServicesApi.md#service_services_v1_identifier_put) | **PUT** /services/v1/{identifier} | Service
[**service_services_v1_post**](ServicesApi.md#service_services_v1_post) | **POST** /services/v1 | Service

# **count_of_services_counts_services_v1_get**
> object count_of_services_counts_services_v1_get()

Count Of Services

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ServicesApi()

try:
    # Count Of Services
    api_response = api_instance.count_of_services_counts_services_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ServicesApi->count_of_services_counts_services_v1_get: %s\n" % e)
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

# **list_services_platforms_platform_services_v1_get**
> object list_services_platforms_platform_services_v1_get(platform, schema=schema, offset=offset, limit=limit)

List Services

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ServicesApi()
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Services
    api_response = api_instance.list_services_platforms_platform_services_v1_get(platform, schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ServicesApi->list_services_platforms_platform_services_v1_get: %s\n" % e)
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

# **list_services_services_v1_get**
> object list_services_services_v1_get(schema=schema, offset=offset, limit=limit)

List Services

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ServicesApi()
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Services
    api_response = api_instance.list_services_services_v1_get(schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ServicesApi->list_services_services_v1_get: %s\n" % e)
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

# **service_platforms_platform_services_v1_identifier_get**
> ServiceRead service_platforms_platform_services_v1_identifier_get(identifier, platform, schema=schema)

Service

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ServicesApi()
identifier = NULL # object | 
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Service
    api_response = api_instance.service_platforms_platform_services_v1_identifier_get(identifier, platform, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ServicesApi->service_platforms_platform_services_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **platform** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**ServiceRead**](ServiceRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **service_services_v1_identifier_delete**
> object service_services_v1_identifier_delete(identifier)

Service

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ServicesApi(swagger_client.ApiClient(configuration))
identifier = NULL # object | 

try:
    # Service
    api_response = api_instance.service_services_v1_identifier_delete(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ServicesApi->service_services_v1_identifier_delete: %s\n" % e)
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

# **service_services_v1_identifier_get**
> ServiceRead service_services_v1_identifier_get(identifier, schema=schema)

Service

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ServicesApi()
identifier = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Service
    api_response = api_instance.service_services_v1_identifier_get(identifier, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ServicesApi->service_services_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**ServiceRead**](ServiceRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **service_services_v1_identifier_put**
> object service_services_v1_identifier_put(body, identifier)

Service

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ServicesApi(swagger_client.ApiClient(configuration))
body = swagger_client.ServiceCreate() # ServiceCreate | 
identifier = NULL # object | 

try:
    # Service
    api_response = api_instance.service_services_v1_identifier_put(body, identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ServicesApi->service_services_v1_identifier_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ServiceCreate**](ServiceCreate.md)|  | 
 **identifier** | [**object**](.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **service_services_v1_post**
> object service_services_v1_post(body)

Service

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ServicesApi(swagger_client.ApiClient(configuration))
body = swagger_client.ServiceCreate() # ServiceCreate | 

try:
    # Service
    api_response = api_instance.service_services_v1_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ServicesApi->service_services_v1_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ServiceCreate**](ServiceCreate.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

