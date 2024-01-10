# ExperimentRead

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**platform** | **object** | The external platform from which this resource originates. Leave empty if this item originates from AIoD. If platform is not None, the platform_resource_identifier should be set as well. | [optional] 
**platform_resource_identifier** | **object** | A unique identifier issued by the external platform that&#x27;s specified in &#x27;platform&#x27;. Leave empty if this item is not part of an external platform. | [optional] 
**name** | **object** |  | 
**date_published** | **object** | The datetime (utc) on which this resource was first published on an external platform. Note the difference between &#x60;.aiod_entry.date_created&#x60; and &#x60;.date_published&#x60;: the former is automatically set to the datetime the resource was created on AIoD, while the latter can optionally be set to an earlier datetime that the resource was published on an external platform. | [optional] 
**same_as** | **object** | Url of a reference Web page that unambiguously indicates this resource&#x27;s identity. | [optional] 
**is_accessible_for_free** | **object** | A flag to signal that this asset is accessible at no cost. | [optional] 
**version** | **object** | The version of this asset. | [optional] 
**pid** | **object** | A permanent identifier for the model, for example a digital object identifier (DOI). Ideally a url. | [optional] 
**experimental_workflow** | **object** | A human readable description of the overall workflow of the experiment. | [optional] 
**execution_settings** | **object** | A human-readable description of the settings under which the experiment was executed. | [optional] 
**reproducibility_explanation** | **object** | A description of how the output of the experiment matches the experiments in the paper. | [optional] 
**ai_asset_identifier** | **object** |  | [optional] 
**ai_resource_identifier** | **object** | This resource can be identified by its own identifier, but also by the resource_identifier. | [optional] 
**aiod_entry** | [**AIoDEntryRead**](AIoDEntryRead.md) |  | [optional] 
**alternate_name** | **object** | An alias for the item, commonly used for the resource instead of the name. | [optional] 
**application_area** | **object** | The objective of this AI resource. | [optional] 
**badge** | **object** | Labels awarded on the basis of the reproducibility of this experiment. | [optional] 
**citation** | **object** | A bibliographic reference. | [optional] 
**contact** | **object** | Contact information of persons/organisations that can be contacted about this resource. | [optional] 
**creator** | **object** | Contact information of persons/organisations that created this resource. | [optional] 
**description** | [**Text**](Text.md) |  | [optional] 
**distribution** | **object** |  | [optional] 
**has_part** | **object** |  | [optional] 
**industrial_sector** | **object** | A business domain where a resource is or can be used. | [optional] 
**is_part_of** | **object** |  | [optional] 
**keyword** | **object** | Keywords or tags used to describe this resource, providing additional context. | [optional] 
**license** | **object** |  | [optional] 
**media** | **object** | Images or videos depicting the resource or associated with it.  | [optional] 
**note** | **object** | Notes on this AI resource. | [optional] 
**relevant_link** | **object** | URLs of relevant resources. These resources should not be part of AIoD (use relevant_resource otherwise). This field should only be used if there is no more specific field. | [optional] 
**relevant_resource** | **object** |  | [optional] 
**relevant_to** | **object** |  | [optional] 
**research_area** | **object** | The research area is similar to the scientific_domain, but more high-level. | [optional] 
**scientific_domain** | **object** | The scientific domain is related to the methods with which an objective is reached. | [optional] 
**identifier** | **object** |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

