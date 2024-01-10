# swagger_client.NewsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**count_of_news_counts_news_v1_get**](NewsApi.md#count_of_news_counts_news_v1_get) | **GET** /counts/news/v1 | Count Of News
[**list_news_news_v1_get**](NewsApi.md#list_news_news_v1_get) | **GET** /news/v1 | List News
[**list_news_platforms_platform_news_v1_get**](NewsApi.md#list_news_platforms_platform_news_v1_get) | **GET** /platforms/{platform}/news/v1 | List News
[**news_news_v1_identifier_delete**](NewsApi.md#news_news_v1_identifier_delete) | **DELETE** /news/v1/{identifier} | News
[**news_news_v1_identifier_get**](NewsApi.md#news_news_v1_identifier_get) | **GET** /news/v1/{identifier} | News
[**news_news_v1_identifier_put**](NewsApi.md#news_news_v1_identifier_put) | **PUT** /news/v1/{identifier} | News
[**news_news_v1_post**](NewsApi.md#news_news_v1_post) | **POST** /news/v1 | News
[**news_platforms_platform_news_v1_identifier_get**](NewsApi.md#news_platforms_platform_news_v1_identifier_get) | **GET** /platforms/{platform}/news/v1/{identifier} | News

# **count_of_news_counts_news_v1_get**
> object count_of_news_counts_news_v1_get()

Count Of News

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NewsApi()

try:
    # Count Of News
    api_response = api_instance.count_of_news_counts_news_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NewsApi->count_of_news_counts_news_v1_get: %s\n" % e)
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

# **list_news_news_v1_get**
> object list_news_news_v1_get(schema=schema, offset=offset, limit=limit)

List News

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NewsApi()
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List News
    api_response = api_instance.list_news_news_v1_get(schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NewsApi->list_news_news_v1_get: %s\n" % e)
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

# **list_news_platforms_platform_news_v1_get**
> object list_news_platforms_platform_news_v1_get(platform, schema=schema, offset=offset, limit=limit)

List News

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NewsApi()
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List News
    api_response = api_instance.list_news_platforms_platform_news_v1_get(platform, schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NewsApi->list_news_platforms_platform_news_v1_get: %s\n" % e)
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

# **news_news_v1_identifier_delete**
> object news_news_v1_identifier_delete(identifier)

News

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.NewsApi(swagger_client.ApiClient(configuration))
identifier = NULL # object | 

try:
    # News
    api_response = api_instance.news_news_v1_identifier_delete(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NewsApi->news_news_v1_identifier_delete: %s\n" % e)
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

# **news_news_v1_identifier_get**
> NewsRead news_news_v1_identifier_get(identifier, schema=schema)

News

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NewsApi()
identifier = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # News
    api_response = api_instance.news_news_v1_identifier_get(identifier, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NewsApi->news_news_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**NewsRead**](NewsRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **news_news_v1_identifier_put**
> object news_news_v1_identifier_put(body, identifier)

News

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.NewsApi(swagger_client.ApiClient(configuration))
body = swagger_client.NewsCreate() # NewsCreate | 
identifier = NULL # object | 

try:
    # News
    api_response = api_instance.news_news_v1_identifier_put(body, identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NewsApi->news_news_v1_identifier_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**NewsCreate**](NewsCreate.md)|  | 
 **identifier** | [**object**](.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **news_news_v1_post**
> object news_news_v1_post(body)

News

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.NewsApi(swagger_client.ApiClient(configuration))
body = swagger_client.NewsCreate() # NewsCreate | 

try:
    # News
    api_response = api_instance.news_news_v1_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NewsApi->news_news_v1_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**NewsCreate**](NewsCreate.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **news_platforms_platform_news_v1_identifier_get**
> NewsRead news_platforms_platform_news_v1_identifier_get(identifier, platform, schema=schema)

News

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NewsApi()
identifier = NULL # object | 
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # News
    api_response = api_instance.news_platforms_platform_news_v1_identifier_get(identifier, platform, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NewsApi->news_platforms_platform_news_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **platform** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**NewsRead**](NewsRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

