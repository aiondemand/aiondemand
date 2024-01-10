# swagger_client.CaseStudiesApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**case_study_case_studies_v1_identifier_content_distribution_idx_get**](CaseStudiesApi.md#case_study_case_studies_v1_identifier_content_distribution_idx_get) | **GET** /case_studies/v1/{identifier}/content/{distribution_idx} | Case Study
[**case_study_case_studies_v1_identifier_content_get**](CaseStudiesApi.md#case_study_case_studies_v1_identifier_content_get) | **GET** /case_studies/v1/{identifier}/content | Case Study
[**case_study_case_studies_v1_identifier_delete**](CaseStudiesApi.md#case_study_case_studies_v1_identifier_delete) | **DELETE** /case_studies/v1/{identifier} | Case Study
[**case_study_case_studies_v1_identifier_get**](CaseStudiesApi.md#case_study_case_studies_v1_identifier_get) | **GET** /case_studies/v1/{identifier} | Case Study
[**case_study_case_studies_v1_identifier_put**](CaseStudiesApi.md#case_study_case_studies_v1_identifier_put) | **PUT** /case_studies/v1/{identifier} | Case Study
[**case_study_case_studies_v1_post**](CaseStudiesApi.md#case_study_case_studies_v1_post) | **POST** /case_studies/v1 | Case Study
[**case_study_platforms_platform_case_studies_v1_identifier_get**](CaseStudiesApi.md#case_study_platforms_platform_case_studies_v1_identifier_get) | **GET** /platforms/{platform}/case_studies/v1/{identifier} | Case Study
[**count_of_case_studies_counts_case_studies_v1_get**](CaseStudiesApi.md#count_of_case_studies_counts_case_studies_v1_get) | **GET** /counts/case_studies/v1 | Count Of Case Studies
[**list_case_studies_case_studies_v1_get**](CaseStudiesApi.md#list_case_studies_case_studies_v1_get) | **GET** /case_studies/v1 | List Case Studies
[**list_case_studies_platforms_platform_case_studies_v1_get**](CaseStudiesApi.md#list_case_studies_platforms_platform_case_studies_v1_get) | **GET** /platforms/{platform}/case_studies/v1 | List Case Studies

# **case_study_case_studies_v1_identifier_content_distribution_idx_get**
> object case_study_case_studies_v1_identifier_content_distribution_idx_get(identifier, distribution_idx, default=default)

Case Study

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.CaseStudiesApi()
identifier = NULL # object | 
distribution_idx = NULL # object | 
default = false # object |  (optional) (default to false)

try:
    # Case Study
    api_response = api_instance.case_study_case_studies_v1_identifier_content_distribution_idx_get(identifier, distribution_idx, default=default)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CaseStudiesApi->case_study_case_studies_v1_identifier_content_distribution_idx_get: %s\n" % e)
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

# **case_study_case_studies_v1_identifier_content_get**
> object case_study_case_studies_v1_identifier_content_get(identifier)

Case Study

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.CaseStudiesApi()
identifier = NULL # object | 

try:
    # Case Study
    api_response = api_instance.case_study_case_studies_v1_identifier_content_get(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CaseStudiesApi->case_study_case_studies_v1_identifier_content_get: %s\n" % e)
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

# **case_study_case_studies_v1_identifier_delete**
> object case_study_case_studies_v1_identifier_delete(identifier)

Case Study

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.CaseStudiesApi(swagger_client.ApiClient(configuration))
identifier = NULL # object | 

try:
    # Case Study
    api_response = api_instance.case_study_case_studies_v1_identifier_delete(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CaseStudiesApi->case_study_case_studies_v1_identifier_delete: %s\n" % e)
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

# **case_study_case_studies_v1_identifier_get**
> CaseStudyRead case_study_case_studies_v1_identifier_get(identifier, schema=schema)

Case Study

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.CaseStudiesApi()
identifier = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Case Study
    api_response = api_instance.case_study_case_studies_v1_identifier_get(identifier, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CaseStudiesApi->case_study_case_studies_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**CaseStudyRead**](CaseStudyRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **case_study_case_studies_v1_identifier_put**
> object case_study_case_studies_v1_identifier_put(body, identifier)

Case Study

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.CaseStudiesApi(swagger_client.ApiClient(configuration))
body = swagger_client.CaseStudyCreate() # CaseStudyCreate | 
identifier = NULL # object | 

try:
    # Case Study
    api_response = api_instance.case_study_case_studies_v1_identifier_put(body, identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CaseStudiesApi->case_study_case_studies_v1_identifier_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CaseStudyCreate**](CaseStudyCreate.md)|  | 
 **identifier** | [**object**](.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **case_study_case_studies_v1_post**
> object case_study_case_studies_v1_post(body)

Case Study

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.CaseStudiesApi(swagger_client.ApiClient(configuration))
body = swagger_client.CaseStudyCreate() # CaseStudyCreate | 

try:
    # Case Study
    api_response = api_instance.case_study_case_studies_v1_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CaseStudiesApi->case_study_case_studies_v1_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CaseStudyCreate**](CaseStudyCreate.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **case_study_platforms_platform_case_studies_v1_identifier_get**
> CaseStudyRead case_study_platforms_platform_case_studies_v1_identifier_get(identifier, platform, schema=schema)

Case Study

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.CaseStudiesApi()
identifier = NULL # object | 
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Case Study
    api_response = api_instance.case_study_platforms_platform_case_studies_v1_identifier_get(identifier, platform, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CaseStudiesApi->case_study_platforms_platform_case_studies_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **platform** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**CaseStudyRead**](CaseStudyRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **count_of_case_studies_counts_case_studies_v1_get**
> object count_of_case_studies_counts_case_studies_v1_get()

Count Of Case Studies

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.CaseStudiesApi()

try:
    # Count Of Case Studies
    api_response = api_instance.count_of_case_studies_counts_case_studies_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CaseStudiesApi->count_of_case_studies_counts_case_studies_v1_get: %s\n" % e)
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

# **list_case_studies_case_studies_v1_get**
> object list_case_studies_case_studies_v1_get(schema=schema, offset=offset, limit=limit)

List Case Studies

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.CaseStudiesApi()
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Case Studies
    api_response = api_instance.list_case_studies_case_studies_v1_get(schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CaseStudiesApi->list_case_studies_case_studies_v1_get: %s\n" % e)
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

# **list_case_studies_platforms_platform_case_studies_v1_get**
> object list_case_studies_platforms_platform_case_studies_v1_get(platform, schema=schema, offset=offset, limit=limit)

List Case Studies

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.CaseStudiesApi()
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Case Studies
    api_response = api_instance.list_case_studies_platforms_platform_case_studies_v1_get(platform, schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CaseStudiesApi->list_case_studies_platforms_platform_case_studies_v1_get: %s\n" % e)
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

