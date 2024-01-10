# swagger_client.EventsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**count_of_events_counts_events_v1_get**](EventsApi.md#count_of_events_counts_events_v1_get) | **GET** /counts/events/v1 | Count Of Events
[**event_events_v1_identifier_delete**](EventsApi.md#event_events_v1_identifier_delete) | **DELETE** /events/v1/{identifier} | Event
[**event_events_v1_identifier_get**](EventsApi.md#event_events_v1_identifier_get) | **GET** /events/v1/{identifier} | Event
[**event_events_v1_identifier_put**](EventsApi.md#event_events_v1_identifier_put) | **PUT** /events/v1/{identifier} | Event
[**event_events_v1_post**](EventsApi.md#event_events_v1_post) | **POST** /events/v1 | Event
[**event_platforms_platform_events_v1_identifier_get**](EventsApi.md#event_platforms_platform_events_v1_identifier_get) | **GET** /platforms/{platform}/events/v1/{identifier} | Event
[**list_events_events_v1_get**](EventsApi.md#list_events_events_v1_get) | **GET** /events/v1 | List Events
[**list_events_platforms_platform_events_v1_get**](EventsApi.md#list_events_platforms_platform_events_v1_get) | **GET** /platforms/{platform}/events/v1 | List Events

# **count_of_events_counts_events_v1_get**
> object count_of_events_counts_events_v1_get()

Count Of Events

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EventsApi()

try:
    # Count Of Events
    api_response = api_instance.count_of_events_counts_events_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EventsApi->count_of_events_counts_events_v1_get: %s\n" % e)
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

# **event_events_v1_identifier_delete**
> object event_events_v1_identifier_delete(identifier)

Event

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.EventsApi(swagger_client.ApiClient(configuration))
identifier = NULL # object | 

try:
    # Event
    api_response = api_instance.event_events_v1_identifier_delete(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EventsApi->event_events_v1_identifier_delete: %s\n" % e)
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

# **event_events_v1_identifier_get**
> EventRead event_events_v1_identifier_get(identifier, schema=schema)

Event

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EventsApi()
identifier = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Event
    api_response = api_instance.event_events_v1_identifier_get(identifier, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EventsApi->event_events_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**EventRead**](EventRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **event_events_v1_identifier_put**
> object event_events_v1_identifier_put(body, identifier)

Event

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.EventsApi(swagger_client.ApiClient(configuration))
body = swagger_client.EventCreate() # EventCreate | 
identifier = NULL # object | 

try:
    # Event
    api_response = api_instance.event_events_v1_identifier_put(body, identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EventsApi->event_events_v1_identifier_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EventCreate**](EventCreate.md)|  | 
 **identifier** | [**object**](.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **event_events_v1_post**
> object event_events_v1_post(body)

Event

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.EventsApi(swagger_client.ApiClient(configuration))
body = swagger_client.EventCreate() # EventCreate | 

try:
    # Event
    api_response = api_instance.event_events_v1_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EventsApi->event_events_v1_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EventCreate**](EventCreate.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **event_platforms_platform_events_v1_identifier_get**
> EventRead event_platforms_platform_events_v1_identifier_get(identifier, platform, schema=schema)

Event

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EventsApi()
identifier = NULL # object | 
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Event
    api_response = api_instance.event_platforms_platform_events_v1_identifier_get(identifier, platform, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EventsApi->event_platforms_platform_events_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **platform** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**EventRead**](EventRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_events_events_v1_get**
> object list_events_events_v1_get(schema=schema, offset=offset, limit=limit)

List Events

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EventsApi()
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Events
    api_response = api_instance.list_events_events_v1_get(schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EventsApi->list_events_events_v1_get: %s\n" % e)
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

# **list_events_platforms_platform_events_v1_get**
> object list_events_platforms_platform_events_v1_get(platform, schema=schema, offset=offset, limit=limit)

List Events

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EventsApi()
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Events
    api_response = api_instance.list_events_platforms_platform_events_v1_get(platform, schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EventsApi->list_events_platforms_platform_events_v1_get: %s\n" % e)
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

