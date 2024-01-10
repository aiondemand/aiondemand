# swagger_client.ProjectsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**count_of_projects_counts_projects_v1_get**](ProjectsApi.md#count_of_projects_counts_projects_v1_get) | **GET** /counts/projects/v1 | Count Of Projects
[**list_projects_platforms_platform_projects_v1_get**](ProjectsApi.md#list_projects_platforms_platform_projects_v1_get) | **GET** /platforms/{platform}/projects/v1 | List Projects
[**list_projects_projects_v1_get**](ProjectsApi.md#list_projects_projects_v1_get) | **GET** /projects/v1 | List Projects
[**project_platforms_platform_projects_v1_identifier_get**](ProjectsApi.md#project_platforms_platform_projects_v1_identifier_get) | **GET** /platforms/{platform}/projects/v1/{identifier} | Project
[**project_projects_v1_identifier_delete**](ProjectsApi.md#project_projects_v1_identifier_delete) | **DELETE** /projects/v1/{identifier} | Project
[**project_projects_v1_identifier_get**](ProjectsApi.md#project_projects_v1_identifier_get) | **GET** /projects/v1/{identifier} | Project
[**project_projects_v1_identifier_put**](ProjectsApi.md#project_projects_v1_identifier_put) | **PUT** /projects/v1/{identifier} | Project
[**project_projects_v1_post**](ProjectsApi.md#project_projects_v1_post) | **POST** /projects/v1 | Project

# **count_of_projects_counts_projects_v1_get**
> object count_of_projects_counts_projects_v1_get()

Count Of Projects

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ProjectsApi()

try:
    # Count Of Projects
    api_response = api_instance.count_of_projects_counts_projects_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsApi->count_of_projects_counts_projects_v1_get: %s\n" % e)
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

# **list_projects_platforms_platform_projects_v1_get**
> object list_projects_platforms_platform_projects_v1_get(platform, schema=schema, offset=offset, limit=limit)

List Projects

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ProjectsApi()
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Projects
    api_response = api_instance.list_projects_platforms_platform_projects_v1_get(platform, schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsApi->list_projects_platforms_platform_projects_v1_get: %s\n" % e)
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

# **list_projects_projects_v1_get**
> object list_projects_projects_v1_get(schema=schema, offset=offset, limit=limit)

List Projects

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ProjectsApi()
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Projects
    api_response = api_instance.list_projects_projects_v1_get(schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsApi->list_projects_projects_v1_get: %s\n" % e)
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

# **project_platforms_platform_projects_v1_identifier_get**
> ProjectRead project_platforms_platform_projects_v1_identifier_get(identifier, platform, schema=schema)

Project

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ProjectsApi()
identifier = NULL # object | 
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Project
    api_response = api_instance.project_platforms_platform_projects_v1_identifier_get(identifier, platform, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsApi->project_platforms_platform_projects_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **platform** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**ProjectRead**](ProjectRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **project_projects_v1_identifier_delete**
> object project_projects_v1_identifier_delete(identifier)

Project

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ProjectsApi(swagger_client.ApiClient(configuration))
identifier = NULL # object | 

try:
    # Project
    api_response = api_instance.project_projects_v1_identifier_delete(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsApi->project_projects_v1_identifier_delete: %s\n" % e)
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

# **project_projects_v1_identifier_get**
> ProjectRead project_projects_v1_identifier_get(identifier, schema=schema)

Project

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ProjectsApi()
identifier = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Project
    api_response = api_instance.project_projects_v1_identifier_get(identifier, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsApi->project_projects_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**ProjectRead**](ProjectRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **project_projects_v1_identifier_put**
> object project_projects_v1_identifier_put(body, identifier)

Project

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ProjectsApi(swagger_client.ApiClient(configuration))
body = swagger_client.ProjectCreate() # ProjectCreate | 
identifier = NULL # object | 

try:
    # Project
    api_response = api_instance.project_projects_v1_identifier_put(body, identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsApi->project_projects_v1_identifier_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ProjectCreate**](ProjectCreate.md)|  | 
 **identifier** | [**object**](.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **project_projects_v1_post**
> object project_projects_v1_post(body)

Project

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ProjectsApi(swagger_client.ApiClient(configuration))
body = swagger_client.ProjectCreate() # ProjectCreate | 

try:
    # Project
    api_response = api_instance.project_projects_v1_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsApi->project_projects_v1_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ProjectCreate**](ProjectCreate.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

