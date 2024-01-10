# swagger_client.EducationalResourcesApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**count_of_educational_resources_counts_educational_resources_v1_get**](EducationalResourcesApi.md#count_of_educational_resources_counts_educational_resources_v1_get) | **GET** /counts/educational_resources/v1 | Count Of Educational Resources
[**educational_resource_educational_resources_v1_identifier_delete**](EducationalResourcesApi.md#educational_resource_educational_resources_v1_identifier_delete) | **DELETE** /educational_resources/v1/{identifier} | Educational Resource
[**educational_resource_educational_resources_v1_identifier_get**](EducationalResourcesApi.md#educational_resource_educational_resources_v1_identifier_get) | **GET** /educational_resources/v1/{identifier} | Educational Resource
[**educational_resource_educational_resources_v1_identifier_put**](EducationalResourcesApi.md#educational_resource_educational_resources_v1_identifier_put) | **PUT** /educational_resources/v1/{identifier} | Educational Resource
[**educational_resource_educational_resources_v1_post**](EducationalResourcesApi.md#educational_resource_educational_resources_v1_post) | **POST** /educational_resources/v1 | Educational Resource
[**educational_resource_platforms_platform_educational_resources_v1_identifier_get**](EducationalResourcesApi.md#educational_resource_platforms_platform_educational_resources_v1_identifier_get) | **GET** /platforms/{platform}/educational_resources/v1/{identifier} | Educational Resource
[**list_educational_resources_educational_resources_v1_get**](EducationalResourcesApi.md#list_educational_resources_educational_resources_v1_get) | **GET** /educational_resources/v1 | List Educational Resources
[**list_educational_resources_platforms_platform_educational_resources_v1_get**](EducationalResourcesApi.md#list_educational_resources_platforms_platform_educational_resources_v1_get) | **GET** /platforms/{platform}/educational_resources/v1 | List Educational Resources

# **count_of_educational_resources_counts_educational_resources_v1_get**
> object count_of_educational_resources_counts_educational_resources_v1_get()

Count Of Educational Resources

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EducationalResourcesApi()

try:
    # Count Of Educational Resources
    api_response = api_instance.count_of_educational_resources_counts_educational_resources_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EducationalResourcesApi->count_of_educational_resources_counts_educational_resources_v1_get: %s\n" % e)
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

# **educational_resource_educational_resources_v1_identifier_delete**
> object educational_resource_educational_resources_v1_identifier_delete(identifier)

Educational Resource

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.EducationalResourcesApi(swagger_client.ApiClient(configuration))
identifier = NULL # object | 

try:
    # Educational Resource
    api_response = api_instance.educational_resource_educational_resources_v1_identifier_delete(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EducationalResourcesApi->educational_resource_educational_resources_v1_identifier_delete: %s\n" % e)
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

# **educational_resource_educational_resources_v1_identifier_get**
> EducationalResourceRead educational_resource_educational_resources_v1_identifier_get(identifier, schema=schema)

Educational Resource

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EducationalResourcesApi()
identifier = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Educational Resource
    api_response = api_instance.educational_resource_educational_resources_v1_identifier_get(identifier, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EducationalResourcesApi->educational_resource_educational_resources_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**EducationalResourceRead**](EducationalResourceRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **educational_resource_educational_resources_v1_identifier_put**
> object educational_resource_educational_resources_v1_identifier_put(body, identifier)

Educational Resource

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.EducationalResourcesApi(swagger_client.ApiClient(configuration))
body = swagger_client.EducationalResourceCreate() # EducationalResourceCreate | 
identifier = NULL # object | 

try:
    # Educational Resource
    api_response = api_instance.educational_resource_educational_resources_v1_identifier_put(body, identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EducationalResourcesApi->educational_resource_educational_resources_v1_identifier_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EducationalResourceCreate**](EducationalResourceCreate.md)|  | 
 **identifier** | [**object**](.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **educational_resource_educational_resources_v1_post**
> object educational_resource_educational_resources_v1_post(body)

Educational Resource

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.EducationalResourcesApi(swagger_client.ApiClient(configuration))
body = swagger_client.EducationalResourceCreate() # EducationalResourceCreate | 

try:
    # Educational Resource
    api_response = api_instance.educational_resource_educational_resources_v1_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EducationalResourcesApi->educational_resource_educational_resources_v1_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EducationalResourceCreate**](EducationalResourceCreate.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **educational_resource_platforms_platform_educational_resources_v1_identifier_get**
> EducationalResourceRead educational_resource_platforms_platform_educational_resources_v1_identifier_get(identifier, platform, schema=schema)

Educational Resource

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EducationalResourcesApi()
identifier = NULL # object | 
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Educational Resource
    api_response = api_instance.educational_resource_platforms_platform_educational_resources_v1_identifier_get(identifier, platform, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EducationalResourcesApi->educational_resource_platforms_platform_educational_resources_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **platform** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**EducationalResourceRead**](EducationalResourceRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_educational_resources_educational_resources_v1_get**
> object list_educational_resources_educational_resources_v1_get(schema=schema, offset=offset, limit=limit)

List Educational Resources

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EducationalResourcesApi()
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Educational Resources
    api_response = api_instance.list_educational_resources_educational_resources_v1_get(schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EducationalResourcesApi->list_educational_resources_educational_resources_v1_get: %s\n" % e)
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

# **list_educational_resources_platforms_platform_educational_resources_v1_get**
> object list_educational_resources_platforms_platform_educational_resources_v1_get(platform, schema=schema, offset=offset, limit=limit)

List Educational Resources

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EducationalResourcesApi()
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Educational Resources
    api_response = api_instance.list_educational_resources_platforms_platform_educational_resources_v1_get(platform, schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EducationalResourcesApi->list_educational_resources_platforms_platform_educational_resources_v1_get: %s\n" % e)
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

