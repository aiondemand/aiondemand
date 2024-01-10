# swagger_client.ComputationalAssetsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**computational_asset_computational_assets_v1_identifier_delete**](ComputationalAssetsApi.md#computational_asset_computational_assets_v1_identifier_delete) | **DELETE** /computational_assets/v1/{identifier} | Computational Asset
[**computational_asset_computational_assets_v1_identifier_get**](ComputationalAssetsApi.md#computational_asset_computational_assets_v1_identifier_get) | **GET** /computational_assets/v1/{identifier} | Computational Asset
[**computational_asset_computational_assets_v1_identifier_put**](ComputationalAssetsApi.md#computational_asset_computational_assets_v1_identifier_put) | **PUT** /computational_assets/v1/{identifier} | Computational Asset
[**computational_asset_computational_assets_v1_post**](ComputationalAssetsApi.md#computational_asset_computational_assets_v1_post) | **POST** /computational_assets/v1 | Computational Asset
[**computational_asset_platforms_platform_computational_assets_v1_identifier_get**](ComputationalAssetsApi.md#computational_asset_platforms_platform_computational_assets_v1_identifier_get) | **GET** /platforms/{platform}/computational_assets/v1/{identifier} | Computational Asset
[**count_of_computational_assets_counts_computational_assets_v1_get**](ComputationalAssetsApi.md#count_of_computational_assets_counts_computational_assets_v1_get) | **GET** /counts/computational_assets/v1 | Count Of Computational Assets
[**list_computational_assets_computational_assets_v1_get**](ComputationalAssetsApi.md#list_computational_assets_computational_assets_v1_get) | **GET** /computational_assets/v1 | List Computational Assets
[**list_computational_assets_platforms_platform_computational_assets_v1_get**](ComputationalAssetsApi.md#list_computational_assets_platforms_platform_computational_assets_v1_get) | **GET** /platforms/{platform}/computational_assets/v1 | List Computational Assets

# **computational_asset_computational_assets_v1_identifier_delete**
> object computational_asset_computational_assets_v1_identifier_delete(identifier)

Computational Asset

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ComputationalAssetsApi(swagger_client.ApiClient(configuration))
identifier = NULL # object | 

try:
    # Computational Asset
    api_response = api_instance.computational_asset_computational_assets_v1_identifier_delete(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ComputationalAssetsApi->computational_asset_computational_assets_v1_identifier_delete: %s\n" % e)
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

# **computational_asset_computational_assets_v1_identifier_get**
> ComputationalAssetRead computational_asset_computational_assets_v1_identifier_get(identifier, schema=schema)

Computational Asset

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ComputationalAssetsApi()
identifier = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Computational Asset
    api_response = api_instance.computational_asset_computational_assets_v1_identifier_get(identifier, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ComputationalAssetsApi->computational_asset_computational_assets_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**ComputationalAssetRead**](ComputationalAssetRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **computational_asset_computational_assets_v1_identifier_put**
> object computational_asset_computational_assets_v1_identifier_put(body, identifier)

Computational Asset

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ComputationalAssetsApi(swagger_client.ApiClient(configuration))
body = swagger_client.ComputationalAssetCreate() # ComputationalAssetCreate | 
identifier = NULL # object | 

try:
    # Computational Asset
    api_response = api_instance.computational_asset_computational_assets_v1_identifier_put(body, identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ComputationalAssetsApi->computational_asset_computational_assets_v1_identifier_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ComputationalAssetCreate**](ComputationalAssetCreate.md)|  | 
 **identifier** | [**object**](.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **computational_asset_computational_assets_v1_post**
> object computational_asset_computational_assets_v1_post(body)

Computational Asset

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ComputationalAssetsApi(swagger_client.ApiClient(configuration))
body = swagger_client.ComputationalAssetCreate() # ComputationalAssetCreate | 

try:
    # Computational Asset
    api_response = api_instance.computational_asset_computational_assets_v1_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ComputationalAssetsApi->computational_asset_computational_assets_v1_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ComputationalAssetCreate**](ComputationalAssetCreate.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **computational_asset_platforms_platform_computational_assets_v1_identifier_get**
> ComputationalAssetRead computational_asset_platforms_platform_computational_assets_v1_identifier_get(identifier, platform, schema=schema)

Computational Asset

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ComputationalAssetsApi()
identifier = NULL # object | 
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Computational Asset
    api_response = api_instance.computational_asset_platforms_platform_computational_assets_v1_identifier_get(identifier, platform, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ComputationalAssetsApi->computational_asset_platforms_platform_computational_assets_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **platform** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**ComputationalAssetRead**](ComputationalAssetRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **count_of_computational_assets_counts_computational_assets_v1_get**
> object count_of_computational_assets_counts_computational_assets_v1_get()

Count Of Computational Assets

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ComputationalAssetsApi()

try:
    # Count Of Computational Assets
    api_response = api_instance.count_of_computational_assets_counts_computational_assets_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ComputationalAssetsApi->count_of_computational_assets_counts_computational_assets_v1_get: %s\n" % e)
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

# **list_computational_assets_computational_assets_v1_get**
> object list_computational_assets_computational_assets_v1_get(schema=schema, offset=offset, limit=limit)

List Computational Assets

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ComputationalAssetsApi()
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Computational Assets
    api_response = api_instance.list_computational_assets_computational_assets_v1_get(schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ComputationalAssetsApi->list_computational_assets_computational_assets_v1_get: %s\n" % e)
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

# **list_computational_assets_platforms_platform_computational_assets_v1_get**
> object list_computational_assets_platforms_platform_computational_assets_v1_get(platform, schema=schema, offset=offset, limit=limit)

List Computational Assets

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ComputationalAssetsApi()
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Computational Assets
    api_response = api_instance.list_computational_assets_platforms_platform_computational_assets_v1_get(platform, schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ComputationalAssetsApi->list_computational_assets_platforms_platform_computational_assets_v1_get: %s\n" % e)
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

