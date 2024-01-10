# swagger_client.DatasetsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**count_of_datasets_counts_datasets_v1_get**](DatasetsApi.md#count_of_datasets_counts_datasets_v1_get) | **GET** /counts/datasets/v1 | Count Of Datasets
[**dataset_datasets_v1_identifier_content_distribution_idx_get**](DatasetsApi.md#dataset_datasets_v1_identifier_content_distribution_idx_get) | **GET** /datasets/v1/{identifier}/content/{distribution_idx} | Dataset
[**dataset_datasets_v1_identifier_content_get**](DatasetsApi.md#dataset_datasets_v1_identifier_content_get) | **GET** /datasets/v1/{identifier}/content | Dataset
[**dataset_datasets_v1_identifier_delete**](DatasetsApi.md#dataset_datasets_v1_identifier_delete) | **DELETE** /datasets/v1/{identifier} | Dataset
[**dataset_datasets_v1_identifier_get**](DatasetsApi.md#dataset_datasets_v1_identifier_get) | **GET** /datasets/v1/{identifier} | Dataset
[**dataset_datasets_v1_identifier_put**](DatasetsApi.md#dataset_datasets_v1_identifier_put) | **PUT** /datasets/v1/{identifier} | Dataset
[**dataset_datasets_v1_post**](DatasetsApi.md#dataset_datasets_v1_post) | **POST** /datasets/v1 | Dataset
[**dataset_platforms_platform_datasets_v1_identifier_get**](DatasetsApi.md#dataset_platforms_platform_datasets_v1_identifier_get) | **GET** /platforms/{platform}/datasets/v1/{identifier} | Dataset
[**list_datasets_datasets_v1_get**](DatasetsApi.md#list_datasets_datasets_v1_get) | **GET** /datasets/v1 | List Datasets
[**list_datasets_platforms_platform_datasets_v1_get**](DatasetsApi.md#list_datasets_platforms_platform_datasets_v1_get) | **GET** /platforms/{platform}/datasets/v1 | List Datasets

# **count_of_datasets_counts_datasets_v1_get**
> object count_of_datasets_counts_datasets_v1_get()

Count Of Datasets

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DatasetsApi()

try:
    # Count Of Datasets
    api_response = api_instance.count_of_datasets_counts_datasets_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->count_of_datasets_counts_datasets_v1_get: %s\n" % e)
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

# **dataset_datasets_v1_identifier_content_distribution_idx_get**
> object dataset_datasets_v1_identifier_content_distribution_idx_get(identifier, distribution_idx, default=default)

Dataset

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DatasetsApi()
identifier = NULL # object | 
distribution_idx = NULL # object | 
default = false # object |  (optional) (default to false)

try:
    # Dataset
    api_response = api_instance.dataset_datasets_v1_identifier_content_distribution_idx_get(identifier, distribution_idx, default=default)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->dataset_datasets_v1_identifier_content_distribution_idx_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **distribution_idx** | [**object**](.md)|  | 
 **default** | [**object**](.md)|  | [optional] [default to false]

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dataset_datasets_v1_identifier_content_get**
> object dataset_datasets_v1_identifier_content_get(identifier)

Dataset

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DatasetsApi()
identifier = NULL # object | 

try:
    # Dataset
    api_response = api_instance.dataset_datasets_v1_identifier_content_get(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->dataset_datasets_v1_identifier_content_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dataset_datasets_v1_identifier_delete**
> object dataset_datasets_v1_identifier_delete(identifier)

Dataset

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.DatasetsApi(swagger_client.ApiClient(configuration))
identifier = NULL # object | 

try:
    # Dataset
    api_response = api_instance.dataset_datasets_v1_identifier_delete(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->dataset_datasets_v1_identifier_delete: %s\n" % e)
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

# **dataset_datasets_v1_identifier_get**
> object dataset_datasets_v1_identifier_get(identifier, schema=schema)

Dataset

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DatasetsApi()
identifier = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Dataset
    api_response = api_instance.dataset_datasets_v1_identifier_get(identifier, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->dataset_datasets_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dataset_datasets_v1_identifier_put**
> object dataset_datasets_v1_identifier_put(body, identifier)

Dataset

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.DatasetsApi(swagger_client.ApiClient(configuration))
body = swagger_client.DatasetCreate() # DatasetCreate | 
identifier = NULL # object | 

try:
    # Dataset
    api_response = api_instance.dataset_datasets_v1_identifier_put(body, identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->dataset_datasets_v1_identifier_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**DatasetCreate**](DatasetCreate.md)|  | 
 **identifier** | [**object**](.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dataset_datasets_v1_post**
> object dataset_datasets_v1_post(body)

Dataset

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.DatasetsApi(swagger_client.ApiClient(configuration))
body = swagger_client.DatasetCreate() # DatasetCreate | 

try:
    # Dataset
    api_response = api_instance.dataset_datasets_v1_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->dataset_datasets_v1_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**DatasetCreate**](DatasetCreate.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dataset_platforms_platform_datasets_v1_identifier_get**
> object dataset_platforms_platform_datasets_v1_identifier_get(identifier, platform, schema=schema)

Dataset

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DatasetsApi()
identifier = NULL # object | 
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Dataset
    api_response = api_instance.dataset_platforms_platform_datasets_v1_identifier_get(identifier, platform, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->dataset_platforms_platform_datasets_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **platform** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_datasets_datasets_v1_get**
> object list_datasets_datasets_v1_get(schema=schema, offset=offset, limit=limit)

List Datasets

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DatasetsApi()
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Datasets
    api_response = api_instance.list_datasets_datasets_v1_get(schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->list_datasets_datasets_v1_get: %s\n" % e)
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

# **list_datasets_platforms_platform_datasets_v1_get**
> object list_datasets_platforms_platform_datasets_v1_get(platform, schema=schema, offset=offset, limit=limit)

List Datasets

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DatasetsApi()
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Datasets
    api_response = api_instance.list_datasets_platforms_platform_datasets_v1_get(platform, schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetsApi->list_datasets_platforms_platform_datasets_v1_get: %s\n" % e)
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

