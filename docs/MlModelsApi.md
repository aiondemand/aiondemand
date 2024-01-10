# swagger_client.MlModelsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**count_of_ml_models_counts_ml_models_v1_get**](MlModelsApi.md#count_of_ml_models_counts_ml_models_v1_get) | **GET** /counts/ml_models/v1 | Count Of Ml Models
[**list_ml_models_ml_models_v1_get**](MlModelsApi.md#list_ml_models_ml_models_v1_get) | **GET** /ml_models/v1 | List Ml Models
[**list_ml_models_platforms_platform_ml_models_v1_get**](MlModelsApi.md#list_ml_models_platforms_platform_ml_models_v1_get) | **GET** /platforms/{platform}/ml_models/v1 | List Ml Models
[**ml_model_ml_models_v1_identifier_content_distribution_idx_get**](MlModelsApi.md#ml_model_ml_models_v1_identifier_content_distribution_idx_get) | **GET** /ml_models/v1/{identifier}/content/{distribution_idx} | Ml Model
[**ml_model_ml_models_v1_identifier_content_get**](MlModelsApi.md#ml_model_ml_models_v1_identifier_content_get) | **GET** /ml_models/v1/{identifier}/content | Ml Model
[**ml_model_ml_models_v1_identifier_delete**](MlModelsApi.md#ml_model_ml_models_v1_identifier_delete) | **DELETE** /ml_models/v1/{identifier} | Ml Model
[**ml_model_ml_models_v1_identifier_get**](MlModelsApi.md#ml_model_ml_models_v1_identifier_get) | **GET** /ml_models/v1/{identifier} | Ml Model
[**ml_model_ml_models_v1_identifier_put**](MlModelsApi.md#ml_model_ml_models_v1_identifier_put) | **PUT** /ml_models/v1/{identifier} | Ml Model
[**ml_model_ml_models_v1_post**](MlModelsApi.md#ml_model_ml_models_v1_post) | **POST** /ml_models/v1 | Ml Model
[**ml_model_platforms_platform_ml_models_v1_identifier_get**](MlModelsApi.md#ml_model_platforms_platform_ml_models_v1_identifier_get) | **GET** /platforms/{platform}/ml_models/v1/{identifier} | Ml Model

# **count_of_ml_models_counts_ml_models_v1_get**
> object count_of_ml_models_counts_ml_models_v1_get()

Count Of Ml Models

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MlModelsApi()

try:
    # Count Of Ml Models
    api_response = api_instance.count_of_ml_models_counts_ml_models_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MlModelsApi->count_of_ml_models_counts_ml_models_v1_get: %s\n" % e)
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

# **list_ml_models_ml_models_v1_get**
> object list_ml_models_ml_models_v1_get(schema=schema, offset=offset, limit=limit)

List Ml Models

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MlModelsApi()
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Ml Models
    api_response = api_instance.list_ml_models_ml_models_v1_get(schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MlModelsApi->list_ml_models_ml_models_v1_get: %s\n" % e)
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

# **list_ml_models_platforms_platform_ml_models_v1_get**
> object list_ml_models_platforms_platform_ml_models_v1_get(platform, schema=schema, offset=offset, limit=limit)

List Ml Models

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MlModelsApi()
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Ml Models
    api_response = api_instance.list_ml_models_platforms_platform_ml_models_v1_get(platform, schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MlModelsApi->list_ml_models_platforms_platform_ml_models_v1_get: %s\n" % e)
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

# **ml_model_ml_models_v1_identifier_content_distribution_idx_get**
> object ml_model_ml_models_v1_identifier_content_distribution_idx_get(identifier, distribution_idx, default=default)

Ml Model

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MlModelsApi()
identifier = NULL # object | 
distribution_idx = NULL # object | 
default = false # object |  (optional) (default to false)

try:
    # Ml Model
    api_response = api_instance.ml_model_ml_models_v1_identifier_content_distribution_idx_get(identifier, distribution_idx, default=default)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MlModelsApi->ml_model_ml_models_v1_identifier_content_distribution_idx_get: %s\n" % e)
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

# **ml_model_ml_models_v1_identifier_content_get**
> object ml_model_ml_models_v1_identifier_content_get(identifier)

Ml Model

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MlModelsApi()
identifier = NULL # object | 

try:
    # Ml Model
    api_response = api_instance.ml_model_ml_models_v1_identifier_content_get(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MlModelsApi->ml_model_ml_models_v1_identifier_content_get: %s\n" % e)
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

# **ml_model_ml_models_v1_identifier_delete**
> object ml_model_ml_models_v1_identifier_delete(identifier)

Ml Model

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.MlModelsApi(swagger_client.ApiClient(configuration))
identifier = NULL # object | 

try:
    # Ml Model
    api_response = api_instance.ml_model_ml_models_v1_identifier_delete(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MlModelsApi->ml_model_ml_models_v1_identifier_delete: %s\n" % e)
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

# **ml_model_ml_models_v1_identifier_get**
> MLModelRead ml_model_ml_models_v1_identifier_get(identifier, schema=schema)

Ml Model

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MlModelsApi()
identifier = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Ml Model
    api_response = api_instance.ml_model_ml_models_v1_identifier_get(identifier, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MlModelsApi->ml_model_ml_models_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**MLModelRead**](MLModelRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ml_model_ml_models_v1_identifier_put**
> object ml_model_ml_models_v1_identifier_put(body, identifier)

Ml Model

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.MlModelsApi(swagger_client.ApiClient(configuration))
body = swagger_client.MLModelCreate() # MLModelCreate | 
identifier = NULL # object | 

try:
    # Ml Model
    api_response = api_instance.ml_model_ml_models_v1_identifier_put(body, identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MlModelsApi->ml_model_ml_models_v1_identifier_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**MLModelCreate**](MLModelCreate.md)|  | 
 **identifier** | [**object**](.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ml_model_ml_models_v1_post**
> object ml_model_ml_models_v1_post(body)

Ml Model

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.MlModelsApi(swagger_client.ApiClient(configuration))
body = swagger_client.MLModelCreate() # MLModelCreate | 

try:
    # Ml Model
    api_response = api_instance.ml_model_ml_models_v1_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MlModelsApi->ml_model_ml_models_v1_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**MLModelCreate**](MLModelCreate.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ml_model_platforms_platform_ml_models_v1_identifier_get**
> MLModelRead ml_model_platforms_platform_ml_models_v1_identifier_get(identifier, platform, schema=schema)

Ml Model

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MlModelsApi()
identifier = NULL # object | 
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Ml Model
    api_response = api_instance.ml_model_platforms_platform_ml_models_v1_identifier_get(identifier, platform, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MlModelsApi->ml_model_platforms_platform_ml_models_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **platform** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**MLModelRead**](MLModelRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

