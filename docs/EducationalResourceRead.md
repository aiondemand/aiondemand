# EducationalResourceRead

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**platform** | **object** | The external platform from which this resource originates. Leave empty if this item originates from AIoD. If platform is not None, the platform_resource_identifier should be set as well. | [optional] 
**platform_resource_identifier** | **object** | A unique identifier issued by the external platform that&#x27;s specified in &#x27;platform&#x27;. Leave empty if this item is not part of an external platform. | [optional] 
**name** | **object** |  | 
**date_published** | **object** | The datetime (utc) on which this resource was first published on an external platform. Note the difference between &#x60;.aiod_entry.date_created&#x60; and &#x60;.date_published&#x60;: the former is automatically set to the datetime the resource was created on AIoD, while the latter can optionally be set to an earlier datetime that the resource was published on an external platform. | [optional] 
**same_as** | **object** | Url of a reference Web page that unambiguously indicates this resource&#x27;s identity. | [optional] 
**time_required** | **object** | An approximate or recommendation of the time required to use or complete the educational resource. | [optional] 
**access_mode** | **object** | The primary mode of accessing this educational resource. | [optional] 
**ai_resource_identifier** | **object** | This resource can be identified by its own identifier, but also by the resource_identifier. | [optional] 
**aiod_entry** | [**AIoDEntryRead**](AIoDEntryRead.md) |  | [optional] 
**alternate_name** | **object** | An alias for the item, commonly used for the resource instead of the name. | [optional] 
**application_area** | **object** | The objective of this AI resource. | [optional] 
**contact** | **object** | Contact information of persons/organisations that can be contacted about this resource. | [optional] 
**content** | [**Text**](Text.md) |  | [optional] 
**creator** | **object** | Contact information of persons/organisations that created this resource. | [optional] 
**description** | [**Text**](Text.md) |  | [optional] 
**educational_level** | **object** | The level or levels of education for which this resource is intended. | [optional] 
**has_part** | **object** |  | [optional] 
**in_language** | **object** | The language(s) of the educational resource, in ISO639-3. | [optional] 
**industrial_sector** | **object** | A business domain where a resource is or can be used. | [optional] 
**is_part_of** | **object** |  | [optional] 
**keyword** | **object** | Keywords or tags used to describe this resource, providing additional context. | [optional] 
**location** | **object** |  | [optional] 
**media** | **object** | Images or videos depicting the resource or associated with it.  | [optional] 
**note** | **object** | Notes on this AI resource. | [optional] 
**pace** | **object** | The high-level study schedule available for this educational resource. \&quot;self-paced\&quot; is mostly used for MOOCS, Tutorials and short courses without interactive elements; \&quot;scheduled\&quot; is used for scheduled courses with interactive elements that is not a full-time engagement; \&quot;full-time\&quot; is used for programmes or intensive courses that require a full-time engagement from the student. | [optional] 
**prerequisite** | **object** | Minimum or recommended requirements to make use of this educational resource. | [optional] 
**relevant_link** | **object** | URLs of relevant resources. These resources should not be part of AIoD (use relevant_resource otherwise). This field should only be used if there is no more specific field. | [optional] 
**relevant_resource** | **object** |  | [optional] 
**relevant_to** | **object** |  | [optional] 
**research_area** | **object** | The research area is similar to the scientific_domain, but more high-level. | [optional] 
**scientific_domain** | **object** | The scientific domain is related to the methods with which an objective is reached. | [optional] 
**target_audience** | **object** | The intended users of this educational resource. | [optional] 
**type** | **object** | The type of educational resource. | [optional] 
**identifier** | **object** |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

