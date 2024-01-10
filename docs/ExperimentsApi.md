# swagger_client.ExperimentsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**count_of_experiments_counts_experiments_v1_get**](ExperimentsApi.md#count_of_experiments_counts_experiments_v1_get) | **GET** /counts/experiments/v1 | Count Of Experiments
[**experiment_experiments_v1_identifier_content_distribution_idx_get**](ExperimentsApi.md#experiment_experiments_v1_identifier_content_distribution_idx_get) | **GET** /experiments/v1/{identifier}/content/{distribution_idx} | Experiment
[**experiment_experiments_v1_identifier_content_get**](ExperimentsApi.md#experiment_experiments_v1_identifier_content_get) | **GET** /experiments/v1/{identifier}/content | Experiment
[**experiment_experiments_v1_identifier_delete**](ExperimentsApi.md#experiment_experiments_v1_identifier_delete) | **DELETE** /experiments/v1/{identifier} | Experiment
[**experiment_experiments_v1_identifier_get**](ExperimentsApi.md#experiment_experiments_v1_identifier_get) | **GET** /experiments/v1/{identifier} | Experiment
[**experiment_experiments_v1_identifier_put**](ExperimentsApi.md#experiment_experiments_v1_identifier_put) | **PUT** /experiments/v1/{identifier} | Experiment
[**experiment_experiments_v1_post**](ExperimentsApi.md#experiment_experiments_v1_post) | **POST** /experiments/v1 | Experiment
[**experiment_platforms_platform_experiments_v1_identifier_get**](ExperimentsApi.md#experiment_platforms_platform_experiments_v1_identifier_get) | **GET** /platforms/{platform}/experiments/v1/{identifier} | Experiment
[**list_experiments_experiments_v1_get**](ExperimentsApi.md#list_experiments_experiments_v1_get) | **GET** /experiments/v1 | List Experiments
[**list_experiments_platforms_platform_experiments_v1_get**](ExperimentsApi.md#list_experiments_platforms_platform_experiments_v1_get) | **GET** /platforms/{platform}/experiments/v1 | List Experiments

# **count_of_experiments_counts_experiments_v1_get**
> object count_of_experiments_counts_experiments_v1_get()

Count Of Experiments

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentsApi()

try:
    # Count Of Experiments
    api_response = api_instance.count_of_experiments_counts_experiments_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentsApi->count_of_experiments_counts_experiments_v1_get: %s\n" % e)
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

# **experiment_experiments_v1_identifier_content_distribution_idx_get**
> object experiment_experiments_v1_identifier_content_distribution_idx_get(identifier, distribution_idx, default=default)

Experiment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentsApi()
identifier = NULL # object | 
distribution_idx = NULL # object | 
default = false # object |  (optional) (default to false)

try:
    # Experiment
    api_response = api_instance.experiment_experiments_v1_identifier_content_distribution_idx_get(identifier, distribution_idx, default=default)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentsApi->experiment_experiments_v1_identifier_content_distribution_idx_get: %s\n" % e)
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

# **experiment_experiments_v1_identifier_content_get**
> object experiment_experiments_v1_identifier_content_get(identifier)

Experiment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentsApi()
identifier = NULL # object | 

try:
    # Experiment
    api_response = api_instance.experiment_experiments_v1_identifier_content_get(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentsApi->experiment_experiments_v1_identifier_content_get: %s\n" % e)
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

# **experiment_experiments_v1_identifier_delete**
> object experiment_experiments_v1_identifier_delete(identifier)

Experiment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ExperimentsApi(swagger_client.ApiClient(configuration))
identifier = NULL # object | 

try:
    # Experiment
    api_response = api_instance.experiment_experiments_v1_identifier_delete(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentsApi->experiment_experiments_v1_identifier_delete: %s\n" % e)
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

# **experiment_experiments_v1_identifier_get**
> ExperimentRead experiment_experiments_v1_identifier_get(identifier, schema=schema)

Experiment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentsApi()
identifier = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Experiment
    api_response = api_instance.experiment_experiments_v1_identifier_get(identifier, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentsApi->experiment_experiments_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**ExperimentRead**](ExperimentRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **experiment_experiments_v1_identifier_put**
> object experiment_experiments_v1_identifier_put(body, identifier)

Experiment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ExperimentsApi(swagger_client.ApiClient(configuration))
body = swagger_client.ExperimentCreate() # ExperimentCreate | 
identifier = NULL # object | 

try:
    # Experiment
    api_response = api_instance.experiment_experiments_v1_identifier_put(body, identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentsApi->experiment_experiments_v1_identifier_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ExperimentCreate**](ExperimentCreate.md)|  | 
 **identifier** | [**object**](.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **experiment_experiments_v1_post**
> object experiment_experiments_v1_post(body)

Experiment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ExperimentsApi(swagger_client.ApiClient(configuration))
body = swagger_client.ExperimentCreate() # ExperimentCreate | 

try:
    # Experiment
    api_response = api_instance.experiment_experiments_v1_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentsApi->experiment_experiments_v1_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ExperimentCreate**](ExperimentCreate.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **experiment_platforms_platform_experiments_v1_identifier_get**
> ExperimentRead experiment_platforms_platform_experiments_v1_identifier_get(identifier, platform, schema=schema)

Experiment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentsApi()
identifier = NULL # object | 
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Experiment
    api_response = api_instance.experiment_platforms_platform_experiments_v1_identifier_get(identifier, platform, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentsApi->experiment_platforms_platform_experiments_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **platform** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**ExperimentRead**](ExperimentRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_experiments_experiments_v1_get**
> object list_experiments_experiments_v1_get(schema=schema, offset=offset, limit=limit)

List Experiments

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentsApi()
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Experiments
    api_response = api_instance.list_experiments_experiments_v1_get(schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentsApi->list_experiments_experiments_v1_get: %s\n" % e)
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

# **list_experiments_platforms_platform_experiments_v1_get**
> object list_experiments_platforms_platform_experiments_v1_get(platform, schema=schema, offset=offset, limit=limit)

List Experiments

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ExperimentsApi()
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Experiments
    api_response = api_instance.list_experiments_platforms_platform_experiments_v1_get(platform, schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentsApi->list_experiments_platforms_platform_experiments_v1_get: %s\n" % e)
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

