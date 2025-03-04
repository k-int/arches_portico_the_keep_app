from arches.app.models.resource import Resource
from arches.app.models.tile import Tile
from arches.app.models.models import Value
import arches.app.utils.task_management as task_management

from arches_keep_app.utils.bng_conversion import convert

import warnings
import os
import xmltodict
import copy
from django.http import HttpResponse
from datetime import datetime
import json


def process_resource(request):
    if request.method == 'POST':

        body = json.loads(request.body)
        resource_ids = body["resourceid_list"]
        period_string = body["period_string"]

        data_object = {
            'monument_entries': [],
            'admin_areas': [],
            'mon_types': [],
        }

        artifact_graph_id = "343cc20c-2c5a-11e8-90fa-0242ac120005"
        area_graph_id = "979aaf0b-7042-11ea-9674-287fcf6a5e72"
        monument_graph_id = "076f9381-7b00-11e9-8d6b-80000b44d1d9"

        monument_node_ids = {
            'system_refs_id': '325a2f2f-efe4-11eb-9b0c-a87eeabdefba',
            'primary_ref_id': '325a2f33-efe4-11eb-b0bb-a87eeabdefba',
            'legacy_id': '325a441c-efe4-11eb-9283-a87eeabdefba',
            'names_id': '676d47f9-9c1c-11ea-9aa0-f875a44e0e11',
            'name_id': '676d47ff-9c1c-11ea-b07f-f875a44e0e11',
            'descriptions_id': 'ba342e69-b554-11ea-a027-f875a44e0e11',
            'description_type_id': 'ba34557b-b554-11ea-ab95-f875a44e0e11',
            'description_id': 'ba345577-b554-11ea-a9ee-f875a44e0e11',
            'record_type_id': '6ed65604-03d0-11ef-89f3-3736dd7ed53f',
            'national_grid_refs_id': '87d39b2b-f44f-11eb-af5e-a87eeabdefba',
            'national_grid_ref_id': '87d3d7bd-f44f-11eb-b1e4-a87eeabdefba',
            'admin_areas': '87d38725-f44f-11eb-8d4b-a87eeabdefba',
            'area_type': '87d3d7c5-f44f-11eb-8459-a87eeabdefba',
            'area_name': '87d3c3ea-f44f-11eb-b532-a87eeabdefba',
            'construction_phases': '77e8f287-efdc-11eb-a790-a87eeabdefba',
            'monument_types': '77e90834-efdc-11eb-b2b9-a87eeabdefba',
            'date_start': '77e8f28e-efdc-11eb-b9f5-a87eeabdefba',
            'date_end': '77e8f29f-efdc-11eb-a58e-a87eeabdefba',
            'date_certainty': '77e8f298-efdc-11eb-9465-a87eeabdefba',
            'date_qualifier': '77e8f294-efdc-11eb-a9a2-a87eeabdefba',
            'type_certainty': '77e9065e-efdc-11eb-baa2-a87eeabdefba',
            'geometry_node_id': "87d3872b-f44f-11eb-bd0c-a87eeabdefba",
            'feature_shape_id': "87d39b39-f44f-11eb-9b17-a87eeabdefba"
        }

        artifact_node_ids = {
            'system_refs_id': 'dd800bc9-b494-11ea-9af8-f875a44e0e11',
            'primary_ref_id': 'dd8032af-b494-11ea-8110-f875a44e0e11',
            'legacy_id': 'dd8032b1-b494-11ea-a183-f875a44e0e11',
            'names_id': '5b0dfb23-7fe2-11ea-bf70-f875a44e0e11',
            'name_id': '5b0dfb27-7fe2-11ea-8ac9-f875a44e0e11',
            'descriptions_id': 'c30977ad-991e-11ea-9368-f875a44e0e11',
            'description_type_id': 'c30977b1-991e-11ea-b259-f875a44e0e11',
            'description_id': 'c30977b0-991e-11ea-ba04-f875a44e0e11',
            'national_grid_refs_id': 'f7cc62ae-f447-11eb-87da-a87eeabdefba',
            'national_grid_ref_id': 'f7ccc89a-f447-11eb-93ce-a87eeabdefba',
            'admin_areas': 'f7cc6299-f447-11eb-b8a3-a87eeabdefba',
            'area_type': 'f7ccc8a2-f447-11eb-9310-a87eeabdefba',
            'area_name': 'f7cca081-f447-11eb-ac78-a87eeabdefba',
            'construction_phases': '99cfca45-381d-11e8-968a-dca90488358a',
            'date_start': '99cfe72e-381d-11e8-882c-dca90488358a',
            'date_end': '99cff7f8-381d-11e8-a059-dca90488358a',
            'date_certainty': '546b1633-3ba4-11eb-a593-f875a44e0e11',
            'date_qualifier': '1d9500e3-0e04-11eb-af9a-f875a44e0e11',
            'geometry_node_id': 'f7cc629f-f447-11eb-b2d3-a87eeabdefba',
            'feature_shape_id': 'f7cc8c75-f447-11eb-953a-a87eeabdefba'
        }

        area_node_ids = {
            'system_refs_id': '8dca12af-edeb-11eb-bc5f-a87eeabdefba',
            'primary_ref_id': '8dca12b3-edeb-11eb-a9ee-a87eeabdefba',
            'legacy_id': '8dca12bd-edeb-11eb-a6c6-a87eeabdefba',
            'names_id': 'f45dbbe3-80b7-11ea-ae0e-f875a44e0e11',
            'name_id': 'f45dbbe8-80b7-11ea-b325-f875a44e0e11',
            'descriptions_id': 'f3cc1681-185b-11eb-927e-f875a44e0e11',
            'description_type_id': 'f3cc1685-185b-11eb-821c-f875a44e0e11',
            'description_id': 'f3cc1684-185b-11eb-9a07-f875a44e0e11',
            'national_grid_refs_id': 'd17a5386-28cd-11eb-972b-f875a44e0e11',
            'national_grid_ref_id': 'd17a7abb-28cd-11eb-81f8-f875a44e0e11',
            'admin_areas': 'd17a538c-28cd-11eb-bb61-f875a44e0e11',
            'area_type': 'd17a7aca-28cd-11eb-bf31-f875a44e0e11',
            'area_name': 'd17a7ab2-28cd-11eb-8ab9-f875a44e0e11',
            'construction_phases': 'b334dddc-4e87-11eb-ab6c-f875a44e0e11',
            'monument_types': 'b334dde6-4e87-11eb-a67c-f875a44e0e11',
            'date_start': '6c2b6c20-4e8a-11eb-bd7f-f875a44e0e11',
            'date_end': '6c2b6c21-4e8a-11eb-95d9-f875a44e0e11',
            'date_certainty': 'f5711ba7-4e8a-11eb-97c3-f875a44e0e11',
            'date_qualifier': '6c2b6c22-4e8a-11eb-82fe-f875a44e0e11',
            'type_certainty': 'b334dddf-4e87-11eb-830e-f875a44e0e11',
            'geometry_node_id': '64be2fdb-3ee5-11eb-9565-f875a44e0e11',
            'feature_shape_id': '64be7e02-3ee5-11eb-8ff0-f875a44e0e11'
        }

        for resource_id in resource_ids:

            try:

                resource = Resource.objects.get(
                    resourceinstanceid = resource_id) 
                resource.load_tiles()

                #### Inclusion checks

                exclude_flag = False

                if str(resource.graph_id) not in [monument_graph_id, artifact_graph_id, area_graph_id]:
                    exclude_flag = True

                if str(resource.graph_id) == monument_graph_id: # monument exclusions
                    for tile in resource.tiles:
                        if str(tile.nodegroup_id) == "6af2a0cb-efc5-11eb-8436-a87eeabdefba": # designation and protection assignment
                            if tile.data["6af2b696-efc5-11eb-b0b5-a87eeabdefba"]: 
                                exclude_flag = True

                        if str(tile.nodegroup_id) == "055b3e3f-04c7-11eb-8d64-f875a44e0e11": # Associated Monuments, Areas or Artefacts
                            if tile.data["055b3e44-04c7-11eb-b131-f875a44e0e11"]:
                                assoc_monument_ids = [assoc_resource["resourceId"] for assoc_resource in tile.data["055b3e44-04c7-11eb-b131-f875a44e0e11"]] # Associated Monument, Area or Artefact
                                for id in assoc_monument_ids:
                                    assoc_resource = Resource.objects.get(
                                        resourceinstanceid = id)
                                    if str(assoc_resource.graph_id) == "b8032b00-594d-11e9-9cf0-18cf5eb368c4": # aircraft monument
                                        exclude_flag = True
                                    if str(assoc_resource.graph_id) == "49bac32e-5464-11e9-a6e2-000d3ab1e588": # maritime vessel
                                        exclude_flag = True

                if str(resource.graph_id) == area_graph_id: # area exclusions
                    for tile in resource.tiles:
                        if str(tile.nodegroup_id) == "a4a81528-efa9-11eb-9abd-a87eeabdefba": # designation and protection assignment
                            exclude_flag = True

                        if str(tile.nodegroup_id) == "d17a5389-28cd-11eb-9670-f875a44e0e11": # area assignment
                            exclude_flag = True

                
                if str(resource.graph_id) == artifact_graph_id: # artefact exclusions
                    for tile in resource.tiles:
                        if str(tile.nodegroup_id) == artifact_node_ids['system_refs_id']:
                            legacy_id = tile.data[artifact_node_ids['legacy_id']]
                            if legacy_id:
                                if "MES" not in legacy_id['en']['value']: # only artefacts with MES in legacy id
                                    exclude_flag = True

                if not exclude_flag:
                    
                    if str(resource.graph_id) == monument_graph_id:
                        id_lookup = monument_node_ids
                    elif str(resource.graph_id) == artifact_graph_id:
                        id_lookup = artifact_node_ids
                    elif str(resource.graph_id) == area_graph_id:
                        id_lookup = area_node_ids

                #### Value assignment

                    #### MonUID1

                    primary_id = None
                    legacy_id = None
                
                    system_refs_tile = Tile.objects.filter(resourceinstance_id = resource.resourceinstanceid, nodegroup_id = id_lookup["system_refs_id"]) 

                    if len(system_refs_tile) == 1:

                        if system_refs_tile[0].data[id_lookup["primary_ref_id"]]:
                            primary_id = system_refs_tile[0].data[id_lookup["primary_ref_id"]]

                        if system_refs_tile[0].data[id_lookup["legacy_id"]]:
                            legacy_id = system_refs_tile[0].data[id_lookup["legacy_id"]]['en']['value']

                    if not primary_id:
                        warnings.warn(f"Warning, resource with id {resource.resourceinstanceid} is missing a primary_id")

                    mon_object = {
                        'MonUID': primary_id,
                        'LegacyID': legacy_id,
                        'ArchesResourceID': resource.resourceinstanceid,
                        'Name': None,
                        'RecordType': None,
                        'Summary': None,
                        'Description': None,
                        'GridRef': None,
                        'Topology': None,
                        'Easting': None,
                        'Northing': None
                    }

                    mon_names = []
                    mon_descriptions =[]
                    mon_summaries = []

                    for tile in resource.tiles: # retrieve id variables

                        if str(tile.nodegroup_id) == id_lookup["names_id"]:  # names
                            monument_name = tile.data[id_lookup["name_id"]]['en']['value']
                            mon_names.append(monument_name)

                        if str(tile.nodegroup_id) == id_lookup["descriptions_id"]:  # descriptions

                            if tile.data[id_lookup["description_type_id"]] == '35508b82-062a-469f-830a-6040c5e5eb8c':  # summary type
                                summary = tile.data[id_lookup["description_id"]]['en']['value']
                                summary = summary.replace("<p>", "")
                                summary = summary.replace("</p>", "")
                                mon_summaries.append(summary)

                            if tile.data[id_lookup["description_type_id"]] == '39a21ebf-7dd6-4a7f-a211-9453202f60aa':  # full type
                                full_description = tile.data[id_lookup["description_id"]]['en']['value']
                                full_description = full_description.replace("<p>", "")
                                full_description = full_description.replace("</p>", "")
                                mon_descriptions.append(full_description)

                        if str(resource.graph_id) == "076f9381-7b00-11e9-8d6b-80000b44d1d9": # monument
                            if str(tile.nodegroup_id) == id_lookup["record_type_id"]:  # resource model type
                                model_type = tile.data[id_lookup["record_type_id"]]
                                model_type_label = "Building" if model_type == "5e5d6f01-fcd9-4ba0-b86d-564456a520b2" else "Monument"
                                mon_object["RecordType"] = model_type_label

                        elif str(resource.graph_id) == "343cc20c-2c5a-11e8-90fa-0242ac120005":
                            mon_object["RecordType"] = "Find Spot"

                        elif str(resource.graph_id) == "979aaf0b-7042-11ea-9674-287fcf6a5e72":
                            mon_object["RecordType"] = "Monument"

                        if str(tile.nodegroup_id) == id_lookup["national_grid_refs_id"]:  # grid reference
                            grid_ref = tile.data[id_lookup["national_grid_ref_id"]]
                            grid_ref_converted = convert(grid_ref)
                            if grid_ref_converted:
                                mon_object["GridRef"] = grid_ref
                                mon_object["Easting"] = grid_ref_converted[0]
                                mon_object["Northing"] = grid_ref_converted[1]

                        if str(tile.nodegroup_id) == id_lookup["geometry_node_id"]:
                            if tile.data[id_lookup['feature_shape_id']]:
                                topology = tile.data[id_lookup['feature_shape_id']]
                                topology_value = Value.objects.get(valueid=topology)
                                mon_object["Topology"] = topology_value.value

                        #### MonUID2
                        if str(tile.nodegroup_id) == id_lookup["admin_areas"]:  

                            admin_area_object = {
                                'MonUID': primary_id,
                                'LegacyID': legacy_id,
                                'AdminAreaType': None,
                                'AdminAreaName': None
                                }

                            area_type = tile.data[id_lookup["area_type"]]
                            area_type_value = Value.objects.get(valueid=area_type) # administrative area type

                            area_type_value_string = "Civil Parish" if area_type_value.value == "Parish" else area_type_value.value

                            area_name = tile.data[id_lookup["area_name"]] # administrative area name
                            area_name_value = Value.objects.get(valueid=area_name)
                            
                            admin_area_object ["AdminAreaType"] = area_type_value_string
                            admin_area_object ["AdminAreaName"] = area_name_value.value
                            
                            data_object["admin_areas"].append(admin_area_object)

                        #### MonUID3 - construction phases

                        if str(tile.nodegroup_id) == id_lookup["construction_phases"]:  # find construction phase

                            monument_type_object = {
                                'UID': str(tile.tileid),
                                'MonUID': primary_id,
                                'LegacyID': legacy_id,
                                'RecType': 'Monument Type',
                                'MonType': None,
                                'FromDate': None,
                                'FromConf': None,
                                'ToDate': None,
                                'ToConf': None,
                                'UnknownDate': None,
                                'TypeConf': None,
                                'DateQualifier': None
                            }

                            if str(resource.graph_id) in ["076f9381-7b00-11e9-8d6b-80000b44d1d9", '979aaf0b-7042-11ea-9674-287fcf6a5e72']: # monument or area
                                
                                monument_types = tile.data[id_lookup["monument_types"]] # monument type
                            
                                monument_types_values = []
                                for monument_type in monument_types:
                                    monument_type_value = Value.objects.get(
                                        valueid=monument_type)
                                    monument_types_values.append(
                                        monument_type_value.value.upper())
                                    
                                monument_types_string = "; ".join(monument_types_values)
                                monument_type_object["MonType"] = monument_types_string

                                type_certainty = tile.data[id_lookup["type_certainty"]] # type confidence
                                if type_certainty == "2d32062f-80b4-4293-94aa-46653ba5c632":
                                    monument_type_object["TypeConf"] = "?"

                            if str(resource.graph_id) == "343cc20c-2c5a-11e8-90fa-0242ac120005":
                                monument_type_object["MonType"] = "FINDSPOT"

                            date_start = tile.data[id_lookup["date_start"]]
                            if isinstance(date_start, str):
                                date_start = date_start.replace("y-", "")
                            monument_type_object["FromDate"] = date_start

                            date_end = tile.data[id_lookup["date_end"]]
                            if isinstance(date_end, str):
                                date_end = date_end.replace("y-", "")
                            monument_type_object["ToDate"] = date_end

                            monument_type_object["UnknownDate"] = 0 if date_start and date_end else 1

                            date_certainty = tile.data[id_lookup["date_certainty"]]
                            date_certainty_value = "?" if date_certainty == "2d32062f-80b4-4293-94aa-46653ba5c632" else ""
                            monument_type_object["FromConf"] = date_certainty_value
                            monument_type_object["ToConf"] = date_certainty_value

                            date_qualifier = tile.data[id_lookup["date_qualifier"]]
                            if date_qualifier: 
                                date_qualifier_value = Value.objects.get(
                                    valueid=date_qualifier)
                                monument_type_object["DateQualifier"] = date_qualifier_value.value
                            
                            if date_start and date_end:
                                data_object["mon_types"].append(monument_type_object)

                        ##### MonUID3 - components

                        if str(resource.graph_id) in ["076f9381-7b00-11e9-8d6b-80000b44d1d9", '979aaf0b-7042-11ea-9674-287fcf6a5e72']: # monument or area
                            if str(tile.nodegroup_id) == "55d6a53e-049c-11eb-8618-f875a44e0e11":  # find components

                                component_types = tile.data["46cd4b7e-049d-11eb-ba3a-f875a44e0e11"]

                                component_types_list = []
                                for component_type in component_types:
                                    component_value = Value.objects.get(valueid=component_type)
                                    component_types_list.append(component_value.value.upper())
                                components_string = "; ".join(component_types_list)

                                construction_phase_tileid = tile.data["a0c7f934-04a4-11eb-9d78-f875a44e0e11"]

                                # find the associated construction phase already stored on the data object
                                construction_phase_obj = None
                                
                                if len(data_object["mon_types"]) > 0: # if there is at least one construction phase stored
                                    for mon_type in data_object["mon_types"]: 
                                        if mon_type['UID'] == construction_phase_tileid: # and if one matches the id on this tile
                                            construction_phase_obj = mon_type

                                    if construction_phase_obj: 
                                        component_obj = copy.deepcopy(construction_phase_obj)
                                        component_obj["MonType"] = components_string
                                        component_obj["RecType"] = "Component Type"
                                        component_obj["UID"] = str(tile.tileid)

                                    data_object["mon_types"].append(component_obj)

                    #### Finish MonUID1
                    if len(mon_names) > 0: 
                        mon_object["Name"] = mon_names[0]
                    if len(mon_summaries) > 0: 
                        mon_object["Summary"] = max(mon_summaries, key=len)
                    if len(mon_descriptions) > 0: 
                        mon_object["Description"] = max(mon_descriptions, key=len)

                    data_object["monument_entries"].append(mon_object)

            except Exception as e:
                print(f"ERROR: whilst processing {resource_id}: {e}")

        xmlxgExportMon = data_object["monument_entries"]
        xmlxgExportMonAdminArea = data_object["admin_areas"]
        xmlxgExportMonTypeDesc = data_object["mon_types"]

        xml_object = {
            "dataroot": {
                "@xmlns:od": "urn:schemas-microsoft-com:officedata",
                "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "@xsi:noNamespaceSchemaLocation": period_string + '.xsd',
                "@generated": datetime.now().isoformat(timespec='seconds'),
                "xmlxgExportMon": xmlxgExportMon,
                "xmlxgExportMonAdminArea": xmlxgExportMonAdminArea,
                "xmlxgExportMonTypeDesc": xmlxgExportMonTypeDesc,
            }}

        xml_string = xmltodict.unparse(xml_object, pretty=True)

        return HttpResponse(xml_string, content_type="application/xml")



