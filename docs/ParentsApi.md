# swagger_client.ParentsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**agent_agents_v1_identifier_get**](ParentsApi.md#agent_agents_v1_identifier_get) | **GET** /agents/v1/{identifier} | Agent
[**ai_asset_ai_assets_v1_identifier_get**](ParentsApi.md#ai_asset_ai_assets_v1_identifier_get) | **GET** /ai_assets/v1/{identifier} | Ai Asset
[**ai_resource_ai_resources_v1_identifier_get**](ParentsApi.md#ai_resource_ai_resources_v1_identifier_get) | **GET** /ai_resources/v1/{identifier} | Ai Resource

# **agent_agents_v1_identifier_get**
> object agent_agents_v1_identifier_get(identifier)

Agent

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ParentsApi()
identifier = NULL # object | 

try:
    # Agent
    api_response = api_instance.agent_agents_v1_identifier_get(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ParentsApi->agent_agents_v1_identifier_get: %s\n" % e)
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

# **ai_asset_ai_assets_v1_identifier_get**
> object ai_asset_ai_assets_v1_identifier_get(identifier)

Ai Asset

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ParentsApi()
identifier = NULL # object | 

try:
    # Ai Asset
    api_response = api_instance.ai_asset_ai_assets_v1_identifier_get(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ParentsApi->ai_asset_ai_assets_v1_identifier_get: %s\n" % e)
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

# **ai_resource_ai_resources_v1_identifier_get**
> object ai_resource_ai_resources_v1_identifier_get(identifier)

Ai Resource

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ParentsApi()
identifier = NULL # object | 

try:
    # Ai Resource
    api_response = api_instance.ai_resource_ai_resources_v1_identifier_get(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ParentsApi->ai_resource_ai_resources_v1_identifier_get: %s\n" % e)
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

