from arches.app.models.resource import Resource
from arches.app.models.models import Value

import xmltodict
import copy
from django.http import JsonResponse
from django.http import HttpResponse
from datetime import datetime
import json

def print_ids(request):
    if request.method == 'POST':

        body = json.loads(request.body)
        print(body)
        resource_ids = body["resourceid_list"]
        period_string = body["period_string"]
        
        resource_object = {
            'monument_entries': [],
            'admin_areas': [],
            'mon_types': [],
        }

        for resource_id in resource_ids:

            resource = Resource.objects.get(
                resourceinstanceid = resource_id) 
            resource.load_tiles()

            #### MONUMENTS

            if str(resource.graph_id) == "076f9381-7b00-11e9-8d6b-80000b44d1d9":

            #### Inclusion checks

                exclude_flag = False

                for tile in resource.tiles:
                    if str(tile.nodegroup_id) == "6af2a0cb-efc5-11eb-8436-a87eeabdefba": # designation and protection assignment
                        if tile.data["6af2b696-efc5-11eb-b0b5-a87eeabdefba"]: 
                            exclude_flag = True

                    if str(tile.nodegroup_id) == "055b3e3f-04c7-11eb-8d64-f875a44e0e11": # Associated Monuments, Areas or Artefacts
                        assoc_monument_ids = [assoc_resource["resourceId"] for assoc_resource in tile.data["055b3e44-04c7-11eb-b131-f875a44e0e11"]] # Associated Monument, Area or Artefact
                        for id in assoc_monument_ids:
                            assoc_resource = Resource.objects.get(
                                resourceinstanceid = id)
                            if str(assoc_resource.graph_id) == "b8032b00-594d-11e9-9cf0-18cf5eb368c4": # aircraft monument
                                exclude_flag = True
                            if str(assoc_resource.graph_id) == "49bac32e-5464-11e9-a6e2-000d3ab1e588": # maritime vessel
                                exclude_flag = True

                if not exclude_flag:
                    
                    #### MonUID1
                
                    mon_object = {
                        'MonUID': str(resource.resourceinstanceid),
                        'PrefRef': str(resource.resourceinstanceid),
                        'Name': None,
                        'RecordType': None,
                        'Summary': None,
                        'Description': None,
                        'GridRef': None
                    }

                    mon_names = []
                    mon_descriptions =[]
                    mon_summaries = []

                    for tile in resource.tiles:

                        if str(tile.nodegroup_id) == "676d47f9-9c1c-11ea-9aa0-f875a44e0e11":  # names
                            monument_name = tile.data["676d47ff-9c1c-11ea-b07f-f875a44e0e11"]['en']['value']
                            mon_names.append(monument_name)

                        if str(tile.nodegroup_id) == "ba342e69-b554-11ea-a027-f875a44e0e11":  # descriptions

                            if tile.data["ba34557b-b554-11ea-ab95-f875a44e0e11"] == '35508b82-062a-469f-830a-6040c5e5eb8c':  # summary type
                                summary = tile.data['ba345577-b554-11ea-a9ee-f875a44e0e11']['en']['value']
                                mon_summaries.append(summary)

                            if tile.data["ba34557b-b554-11ea-ab95-f875a44e0e11"] == '39a21ebf-7dd6-4a7f-a211-9453202f60aa':  # full type
                                full_description = tile.data['ba345577-b554-11ea-a9ee-f875a44e0e11']['en']['value']
                                mon_descriptions.append(full_description)

                        if str(tile.nodegroup_id) == "6ed65604-03d0-11ef-89f3-3736dd7ed53f":  # resource model type
                            model_type = tile.data["6ed65604-03d0-11ef-89f3-3736dd7ed53f"]
                            model_type_label = "Building" if model_type == "5e5d6f01-fcd9-4ba0-b86d-564456a520b2" else "Monument"
                            mon_object["RecordType"] = model_type_label

                        if str(tile.nodegroup_id) == "87d39b2b-f44f-11eb-af5e-a87eeabdefba":  # grid reference
                            mon_object["GridRef"] = tile.data["87d3d7bd-f44f-11eb-b1e4-a87eeabdefba"]

                    if len(mon_names) > 0: mon_object["Name"] = mon_names[0]
                    if len(mon_summaries) > 0: mon_object["Summary"] = mon_summaries[0]
                    if len(mon_descriptions) > 0: mon_object["Description"] = mon_descriptions[0]

                    resource_object["monument_entries"].append(mon_object)

                    #### MonUID2
                    for tile in resource.tiles:

                        if str(tile.nodegroup_id) == "87d38725-f44f-11eb-8d4b-a87eeabdefba":  # administrative area type

                            admin_area_object = {
                                'MonUID': str(resource.resourceinstanceid),
                                'AdminAreaType': None,
                                'AdminAreaName': None
                                }

                            area_type = tile.data["87d3d7c5-f44f-11eb-8459-a87eeabdefba"]
                            area_type_value = Value.objects.get(valueid=area_type)

                            area_name = tile.data["87d3c3ea-f44f-11eb-b532-a87eeabdefba"] # administrative area name
                            area_name_value = Value.objects.get(valueid=area_name)
                            
                            admin_area_object ["AdminAreaType"] = area_type_value.value
                            admin_area_object ["AdminAreaName"] = area_name_value.value
                            
                            resource_object["admin_areas"].append(admin_area_object)

                    #### MonUID3

                    for tile in resource.tiles:
                        if str(tile.nodegroup_id) == "77e8f287-efdc-11eb-a790-a87eeabdefba":  # find construction phase

                            monument_type_object = {
                                'UID': str(tile.tileid),
                                'MonUID': str(resource.resourceinstanceid),
                                'MonTypeDesc': None,
                                'RecType': 'Monument Type',
                                'MonType': None,
                                'FromDate': None,
                                'FromConf': None,
                                'ToDate': None,
                                'ToConf': None,
                                'UnknownDate': None,
                                'TypeConf': None,
                                'Currency': None,
                                'DisplayDate': None,
                                'DateQualifier': None
                            }
                            
                            monument_types = tile.data["77e90834-efdc-11eb-b2b9-a87eeabdefba"] # monument type
                        
                            monument_types_values = []
                            for monument_type in monument_types:
                                monument_type_value = Value.objects.get(
                                    valueid=monument_type)
                                monument_types_values.append(
                                    monument_type_value.value.upper())
                                
                            monument_types_string = "; ".join(monument_types_values)
                            monument_type_object["MonType"] = monument_types_string

                            date_start = tile.data["77e8f28e-efdc-11eb-b9f5-a87eeabdefba"]
                            if isinstance(date_start, str):
                                date_start = date_start.replace("y-", "")
                            monument_type_object["FromDate"] = date_start

                            date_end = tile.data["77e8f29f-efdc-11eb-a58e-a87eeabdefba"]
                            if isinstance(date_end, str):
                                date_end = date_end.replace("y-", "")
                            monument_type_object["ToDate"] = date_end

                            monument_type_object["UnknownDate"] = 0 if date_start and date_end else 1

                            date_certainty = tile.data["77e8f298-efdc-11eb-9465-a87eeabdefba"]
                            date_certainty_value = "?" if date_certainty == "2d32062f-80b4-4293-94aa-46653ba5c632" else ""
                            monument_type_object["FromConf"] = date_certainty_value
                            monument_type_object["ToConf"] = date_certainty_value

                            date_qualifier = tile.data["77e8f294-efdc-11eb-a9a2-a87eeabdefba"]
                            if date_qualifier: 
                                date_qualifier_value = Value.objects.get(
                                    valueid=date_qualifier)
                                monument_type_object["DateQualifier"] = date_qualifier_value.value
                            
                            resource_object["mon_types"].append(monument_type_object)

                    for tile in resource.tiles:
                        if str(tile.nodegroup_id) == "55d6a53e-049c-11eb-8618-f875a44e0e11":  # find components

                            component_types = tile.data["46cd4b7e-049d-11eb-ba3a-f875a44e0e11"]
                            component_types_list = []
                            for component_type in component_types:
                                component_value = Value.objects.get(valueid=component_type)
                                component_types_list.append(component_value.value.upper())
                            components_string = "; ".join(component_types_list)

                            construction_phase_tileid = tile.data["a0c7f934-04a4-11eb-9d78-f875a44e0e11"]
                            construction_phase_obj = [construction_phase for construction_phase in resource_object["mon_types"] if construction_phase["UID"] == construction_phase_tileid][0]

                            component_obj = copy.deepcopy(construction_phase_obj)
                            component_obj["MonTypeDesc"] = components_string
                            component_obj["RecType"] = "Component Type"
                            component_obj["UID"] = str(tile.tileid)

                            resource_object["mon_types"].append(component_obj)

            #### ARTIFACTS

            if str(resource.graph_id) == "343cc20c-2c5a-11e8-90fa-0242ac120005":

            #### Inclusion checks

                exclude_flag = False

                for tile in resource.tiles:
                    if True:
                        exclude_flag = True

                if not exclude_flag:

                    #### MonUID1
            
                    artifact_object = {
                        'MonUID': str(resource.resourceinstanceid),
                        'PrefRef': str(resource.resourceinstanceid),
                        'Name': None,
                        'RecordType': None,
                        'Summary': None,
                        'Description': None,
                        'GridRef': None
                    }

                    artifact_names = []
                    artifact_descriptions =[]
                    artifact_summaries = []

                    for tile in resource.tiles:

                        if str(tile.nodegroup_id) == "5b0dfb23-7fe2-11ea-bf70-f875a44e0e11":  # names
                            artifact_name = tile.data["5b0dfb27-7fe2-11ea-8ac9-f875a44e0e11"]['en']['value']
                            artifact_names.append(artifact_name)

                        if str(tile.nodegroup_id) == "c30977ad-991e-11ea-9368-f875a44e0e11":  # descriptions

                            if tile.data["c30977b1-991e-11ea-b259-f875a44e0e11"] == '35508b82-062a-469f-830a-6040c5e5eb8c':  # summary type
                                summary = tile.data['c30977b0-991e-11ea-ba04-f875a44e0e11']['en']['value']
                                artifact_summaries.append(summary)

                            if tile.data["c30977b1-991e-11ea-b259-f875a44e0e11"] == '39a21ebf-7dd6-4a7f-a211-9453202f60aa':  # full type
                                full_description = tile.data['c30977b0-991e-11ea-ba04-f875a44e0e11']['en']['value']
                                artifact_descriptions.append(full_description)

                        if str(tile.nodegroup_id) == "f7cc62ae-f447-11eb-87da-a87eeabdefba":  # grid reference
                            artifact_object["GridRef"] = tile.data["f7ccc89a-f447-11eb-93ce-a87eeabdefba"]

                    artifact_object["RecordType"] = "Find Spot"
                    if len(artifact_names) > 0: artifact_object["Name"] = artifact_names[0]
                    if len(artifact_summaries) > 0: artifact_object["Summary"] = artifact_summaries[0]
                    if len(artifact_descriptions) > 0: artifact_object["Description"] = artifact_descriptions[0]

                    resource_object["monument_entries"].append(artifact_object)

                    #### MonUID2
                    for tile in resource.tiles:

                        if str(tile.nodegroup_id) == "f7cc6299-f447-11eb-b8a3-a87eeabdefba":  # administrative area type

                            admin_area_object = {
                                'MonUID': str(resource.resourceinstanceid),
                                'AdminAreaType': None,
                                'AdminAreaName': None
                                }

                            area_type = tile.data["f7ccc8a2-f447-11eb-9310-a87eeabdefba"]
                            area_type_value = Value.objects.get(valueid=area_type)

                            area_name = tile.data["f7cca081-f447-11eb-ac78-a87eeabdefba"] # administrative area name
                            area_name_value = Value.objects.get(valueid=area_name)
                            
                            admin_area_object ["AdminAreaType"] = area_type_value.value
                            admin_area_object ["AdminAreaName"] = area_name_value.value
                            
                            resource_object["admin_areas"].append(admin_area_object)

                    #### MonUID3

                    for tile in resource.tiles:
                        if str(tile.nodegroup_id) == "99cfca45-381d-11e8-968a-dca90488358a":  # find construction phase

                            artifact_type_object = {
                                'UID': str(tile.tileid),
                                'MonUID': str(resource.resourceinstanceid),
                                'MonTypeDesc': None,
                                'RecType': 'Monument Type',
                                'MonType': "FINDSPOT",
                                'FromDate': None,
                                'FromConf': None,
                                'ToDate': None,
                                'ToConf': None,
                                'UnknownDate': None,
                                'TypeConf': None,
                                'Currency': None,
                                'DisplayDate': None,
                                'DateQualifier': None
                            }
                            
                            date_start = tile.data["99cfe72e-381d-11e8-882c-dca90488358a"]

                            if isinstance(date_start, str):
                                date_start = date_start.replace("y-", "")
                            artifact_type_object["FromDate"] = date_start

                            date_end = tile.data["99cff7f8-381d-11e8-a059-dca90488358a"]
                            if isinstance(date_end, str):
                                date_end = date_end.replace("y-", "")
                            artifact_type_object["ToDate"] = date_end

                            artifact_type_object["UnknownDate"] = 0 if date_start and date_end else 1

                            date_certainty = tile.data["546b1633-3ba4-11eb-a593-f875a44e0e11"]                   
                            date_certainty_value = "?" if date_certainty == "2d32062f-80b4-4293-94aa-46653ba5c632" else ""

                            artifact_type_object["FromConf"] = date_certainty_value
                            artifact_type_object["ToConf"] = date_certainty_value

                            date_qualifier = tile.data["1d9500e3-0e04-11eb-af9a-f875a44e0e11"]
                            if date_qualifier: 
                                date_qualifier_value = Value.objects.get(
                                    valueid=date_qualifier)
                                artifact_type_object["DateQualifier"] = date_qualifier_value.value
                            
                            resource_object["mon_types"].append(monument_type_object)

            #### AREAS

            if str(resource.graph_id) == "979aaf0b-7042-11ea-9674-287fcf6a5e72":

            #### Inclusion checks

                exclude_flag = False

                for tile in resource.tiles:
                    if str(tile.nodegroup_id) == "a4a81528-efa9-11eb-9abd-a87eeabdefba": # designation and protection assignment
                        exclude_flag = True

                    if str(tile.nodegroup_id) == "d17a5389-28cd-11eb-9670-f875a44e0e11": # area assignment
                        exclude_flag = True

                if not exclude_flag:    

                    #### MonUID1
            
                    area_object = {
                        'MonUID': str(resource.resourceinstanceid),
                        'PrefRef': str(resource.resourceinstanceid),
                        'Name': None,
                        'RecordType': None,
                        'Summary': None,
                        'Description': None,
                        'GridRef': None
                    }

                    area_names = []
                    area_descriptions =[]
                    area_summaries = []

                    for tile in resource.tiles:

                        if str(tile.nodegroup_id) == "f45dbbe3-80b7-11ea-ae0e-f875a44e0e11":  # names
                            area_name = tile.data["f45dbbe8-80b7-11ea-b325-f875a44e0e11"]['en']['value']
                            area_names.append(area_name)

                        if str(tile.nodegroup_id) == "f3cc1681-185b-11eb-927e-f875a44e0e11":  # descriptions

                            if tile.data["f3cc1685-185b-11eb-821c-f875a44e0e11"] == '35508b82-062a-469f-830a-6040c5e5eb8c':  # summary type
                                summary = tile.data['f3cc1684-185b-11eb-9a07-f875a44e0e11']['en']['value']
                                area_summaries.append(summary)

                            if tile.data["f3cc1685-185b-11eb-821c-f875a44e0e11"] == '39a21ebf-7dd6-4a7f-a211-9453202f60aa':  # full type
                                full_description = tile.data['f3cc1684-185b-11eb-9a07-f875a44e0e11']['en']['value']
                                area_descriptions.append(full_description)

                        if str(tile.nodegroup_id) == "d17a5386-28cd-11eb-972b-f875a44e0e11":  # grid reference
                            area_object["GridRef"] = tile.data["d17a7abb-28cd-11eb-81f8-f875a44e0e11"]

                    area_object["RecordType"] = "Monument"
                    if len(area_names) > 0: area_object["Name"] = area_names[0]
                    if len(area_summaries) > 0: area_object["Summary"] = area_summaries[0]
                    if len(area_descriptions) > 0: area_object["Description"] = area_descriptions[0]

                    resource_object["monument_entries"].append(area_object)

                    #### MonUID2
                    for tile in resource.tiles:

                        if str(tile.nodegroup_id) == "d17a538c-28cd-11eb-bb61-f875a44e0e11":  # administrative area type

                            admin_area_object = {
                                'MonUID': str(resource.resourceinstanceid),
                                'AdminAreaType': None,
                                'AdminAreaName': None
                                }

                            area_type = tile.data["d17a7aca-28cd-11eb-bf31-f875a44e0e11"]
                            area_type_value = Value.objects.get(valueid=area_type)

                            area_name = tile.data["d17a7ab2-28cd-11eb-8ab9-f875a44e0e11"] # administrative area name
                            area_name_value = Value.objects.get(valueid=area_name)
                            
                            admin_area_object ["AdminAreaType"] = area_type_value.value
                            admin_area_object ["AdminAreaName"] = area_name_value.value

                            resource_object["admin_areas"].append(admin_area_object)

                    #### MonUID3

                    for tile in resource.tiles:
                        if str(tile.nodegroup_id) == "b334dddc-4e87-11eb-ab6c-f875a44e0e11":  # find construction phase

                            area_type_object = {
                                'UID': str(tile.tileid),
                                'MonUID': str(resource.resourceinstanceid),
                                'MonTypeDesc': None,
                                'RecType': 'Monument Type',
                                'MonType': "FINDSPOT",
                                'FromDate': None,
                                'FromConf': None,
                                'ToDate': None,
                                'ToConf': None,
                                'UnknownDate': None,
                                'TypeConf': None,
                                'Currency': None,
                                'DisplayDate': None,
                                'DateQualifier': None
                            }
                            
                            area_types = tile.data["b334dde6-4e87-11eb-a67c-f875a44e0e11"] # area type

                            area_types_values = []
                            for area_type in area_types:
                                area_type_value = Value.objects.get(
                                    valueid=area_type)
                                area_types_values.append(
                                    area_type_value.value.upper())
                                
                            area_types_string = "; ".join(area_types_values)
                            area_type_object["MonType"] = area_types_string

                            date_start = tile.data["6c2b6c20-4e8a-11eb-bd7f-f875a44e0e11"]

                            if isinstance(date_start, str):
                                date_start = date_start.replace("y-", "")
                            area_type_object["FromDate"] = date_start

                            date_end = tile.data["6c2b6c21-4e8a-11eb-95d9-f875a44e0e11"]
                            if isinstance(date_end, str):
                                date_end = date_end.replace("y-", "")
                            area_type_object["ToDate"] = date_end

                            area_type_object["UnknownDate"] = 0 if date_start and date_end else 1

                            date_certainty = tile.data["f5711ba7-4e8a-11eb-97c3-f875a44e0e11"]                   
                            date_certainty_value = "?" if date_certainty == "2d32062f-80b4-4293-94aa-46653ba5c632" else ""

                            area_type_object["FromConf"] = date_certainty_value
                            area_type_object["ToConf"] = date_certainty_value

                            date_qualifier = tile.data["6c2b6c22-4e8a-11eb-82fe-f875a44e0e11"]
                            if date_qualifier: 
                                date_qualifier_value = Value.objects.get(
                                    valueid=date_qualifier)
                                area_type_object["DateQualifier"] = date_qualifier_value.value
                            
                            resource_object["mon_types"].append(area_type_object)

                    for tile in resource.tiles:
                        if str(tile.nodegroup_id) == "55d6a53e-049c-11eb-8618-f875a44e0e11":  # find components

                            component_types = tile.data["46cd4b7e-049d-11eb-ba3a-f875a44e0e11"]
                            component_types_list = []
                            for component_type in component_types:
                                component_value = Value.objects.get(valueid=component_type)
                                component_types_list.append(component_value.value.upper())
                            components_string = "; ".join(component_types_list)

                            construction_phase_tileid = tile.data["a0c7f934-04a4-11eb-9d78-f875a44e0e11"]
                            construction_phase_obj = [construction_phase for construction_phase in resource_object["mon_types"] if construction_phase["UID"] == construction_phase_tileid][0]

                            component_obj = copy.deepcopy(construction_phase_obj)
                            component_obj["MonTypeDesc"] = components_string
                            component_obj["RecType"] = "Component Type"
                            component_obj["UID"] = str(tile.tileid)

                            resource_object["mon_types"].append(component_obj)    

        xmlxgExportMon = resource_object["monument_entries"]
        xmlxgExportMonAdminArea = resource_object["admin_areas"]
        xmlxgExportMonTypeDesc = resource_object["mon_types"]

        xml_object = {
            "dataroot": {
                "@xmlns:od": "urn:schemas-microsoft-com:officedata",
                "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "@xsi:noNamespaceSchemaLocation": period_string,
                "@generated": datetime.now().isoformat(timespec='seconds'),
                "xmlxgExportMon": xmlxgExportMon,
                "xmlxgExportMonAdminArea": xmlxgExportMonAdminArea,
                "xmlxgExportMonTypeDesc": xmlxgExportMonTypeDesc,
            }}

        xml_string = xmltodict.unparse(xml_object, pretty=True)

        return HttpResponse(xml_string, content_type="application/xml")



