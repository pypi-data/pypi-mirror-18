'''
Created on Apr 3, 2015

@author: nate
'''
import tabulate
import json
import time
from collections import OrderedDict

from utils.converters.volume.recurrence_rule_converter import RecurrenceRuleConverter
from model.health.health_category import HealthCategory
from utils.byte_converter import ByteConverter

class ResponseWriter():
    
    @staticmethod
    def write_not_implemented(args=None):
        print("\nThis feature is not yet available, but the fine people at Formation Data System are working tirelessly to make this a reality in the near future.\n")
    
    @staticmethod
    def writeTabularData( data, headers="keys" ):
        
        if ( len(data) == 0 ):
            return
        else:
            print(tabulate.tabulate( data, headers=headers ))
            print("\n")

        
    @staticmethod
    def writeJson( data ):
        print("\n" + json.dumps( data, indent=4, sort_keys=True ) + "\n")
        
    @staticmethod
    def prep_volume_for_table( session, response ):
        '''
        making the structure table friendly
        '''        
        
        prepped_responses = []
        
        # Some calls return a singular volume instead of a list, but if we put it in a list we can re-use this algorithm
        if ( isinstance( response, dict ) ):
            response = [response]
        
        for volume in response:
            
            #figure out what to show for last firebreak occurrence
            lastFirebreak = int(volume.status.last_capacity_firebreak)
            lastFirebreakType = "Capacity"
            
            if ( int(volume.status.last_performance_firebreak) > lastFirebreak ):
                lastFirebreak = int(volume.status.last_performance_firebreak)
                lastFirebreakType = "Performance"
                
            if ( lastFirebreak == 0 ):
                lastFirebreak = "Never"
                lastFirebreakType = ""
            else:
                lastFirebreak = time.localtime( lastFirebreak )
                lastFirebreak = time.strftime( "%c", lastFirebreak )
            
            #sanitize the IOPs guarantee value
            iopsMin = volume.qos_policy.iops_min
            
            if ( iopsMin == 0 ):
                iopsMin = "None"
                
            #sanitize the IOPs limit
            iopsLimit = volume.qos_policy.iops_max
            
            if ( iopsLimit == 0 ):
                iopsLimit = "Unlimited"

            ov = OrderedDict()
            
            ov["ID"] = volume.id
            ov["Name"] = volume.name
            
            if ( session.is_allowed( "TENANT_MGMT" ) ):
                if volume.tenant is not None:
                    ov["Tenant"] = volume.tenant.name
                else:
                    ov["Tenant"] = ""
                    
                
            ov["State"] = volume.status.state
            ov["Type"] = volume.settings.type
            
            bytesUsed = ByteConverter.convertBytesToString( volume.status.current_usage.get_bytes(), 2 )
            allocated = ""
            
            if hasattr( volume.settings, "capacity"):
                all_str = ByteConverter.convertBytesToString( volume.settings.capacity.size, 0 )
                allocated = " / {}".format( all_str )
            
            ov["Usage"] = bytesUsed + allocated 
            ov["Last Firebreak Type"] = lastFirebreakType
            ov["Last Firebreak"] = lastFirebreak
            ov["Priority"] = volume.qos_policy.priority
            ov["IOPs Guarantee"] = iopsMin
            ov["IOPs Limit"] = iopsLimit
            ov["Media Policy"] = volume.media_policy
            
            prepped_responses.append( ov )
        #end of for loop 
            
        return prepped_responses
    
    @staticmethod
    def prep_snapshot_for_table( session, response ):
        '''
        Take the snapshot response and make it consumable for a table
        '''
        
        #The tabular format is very poor for a volume object, so we need to remove some keys before display
        resultList = []
        
        for snapshot in response:
            
            created = time.localtime( snapshot.created )
            created = time.strftime( "%c", created )
            
            retentionValue = snapshot.retention
            
            if ( retentionValue == 0 ):
                retentionValue = "Forever"
            
            ov = OrderedDict()
            
            ov["ID"] = snapshot.id
            ov["Name"] = snapshot.name
            ov["Created"] = created
            ov["Retention"] = retentionValue
            
            resultList.append( ov )   
        #end for loop
        
        return resultList

    @staticmethod
    def prep_snapshot_policy_for_table( session, response ):
        ''' 
        Take a snapshot policy and format it for easy display in a table
        '''
        
        results = []
        
        for policy in response:
            
            retentionValue = policy.retention_time_in_seconds
            
            if ( retentionValue == 0 ):
                retentionValue = "Forever"
        
            ov = OrderedDict()
            
            if policy.id != None:
                ov["ID"] = policy.id
            
            if ( policy.name != None and policy.name != "" ):
                ov["Name"] = policy.name

            ov["Retention"] = retentionValue
            ov["Recurrence Rule"] = RecurrenceRuleConverter.to_json( policy.recurrence_rule )
            
            results.append( ov )
        # end of for loop
        
        return results
            
    
    @staticmethod
    def prep_domains_for_table( session, response ):
        '''
        Take the domain JSON and turn it into a table worthy presentation
        '''
        results = []
        
        for domain in response:
            
            ov = OrderedDict()
            
            ov["ID"] = domain.id
            ov["Name"] = domain.name
            ov["Site"] = domain.site
            ov["State"] = domain.state
            
            results.append( ov )
        #end of for loop
        
        return results
    
    
    @staticmethod
    def prep_node_for_table( session, response ):
        '''
        Take nodes and format them to be listed in a table
        '''
        
        results = []
        
        for node in response:
            
            ov = OrderedDict()
            
            ov["ID"] = node.id
            ov["Name"] = node.name
            ov["State"] = node.state
            ov["IP V4 Address"] = node.address.ipv4address
            
            results.append( ov )
        
        return results
    
    @staticmethod
    def prep_services_for_table( session, response ):
        '''
        The service model is not yet sensible so we need to do some munging to get anything
        useful to the Screen.
        '''
        results = []
        
        for node in response:
            
            # we'll need this data for each service
            
            services = node.services
            
            for service_type in services:
                
                for service in services[service_type]:
                    
                    ov = OrderedDict()
                    ov["Node ID"] = node.id
                    ov["Node Name"] = node.name
                    ov["Service Type"] = service.name
                    ov["Service ID"] = service.id
                    ov["State"] = service.status.state
                    
                    results.append( ov )
                    
                # end of individual service for loop
            #end of service_typess for loop
            
        #end of nodes for loop
        
        return results

    @staticmethod
    def prep_safeguard_tasks_for_table( session, response ):
        '''Prep a list of SafeGuard task status records for tabular printing
        '''
        results = []

        for task_with_status in response:

            ov = OrderedDict()
            ov["Type"] = str(task_with_status.task_type)
            ov["Volume ID"] = task_with_status.volume_id
            ov["Progress"] = str(task_with_status.status)
            ov["Description"] = task_with_status.description
            ov["Task ID"] = task_with_status.uuid

            results.append( ov )

        return results

    @staticmethod
    def prep_f1credentials_for_table( session, named_credentials ):

        results = []

        for named_credential in named_credentials:

            ov = OrderedDict()
            ov["Named Credential ID"] = named_credential.digest
            ov["Name"] = named_credential.name
            ov["OM Url"] = named_credential.url
            results.append( ov )

        return results

    @staticmethod
    def prep_s3credentials_for_table( session, named_credentials ):

        results = []

        for named_credential in named_credentials:

            ov = OrderedDict()
            ov["Named Credential ID"] = named_credential.digest
            ov["Name"] = named_credential.name
            ov["Url"] = named_credential.url
            ov["Bucket Name"] = named_credential.bucketname
            if named_credential.s3credentials is not None:
                ov["S3 Access Key"] = named_credential.s3credentials.access_key_id
                ov["S3 Secret Key"] = named_credential.s3credentials.secret_key
            results.append( ov )

        return results

    @staticmethod
    def prep_qos_presets( presets):
        '''
        Prep a list of qos presets for tabular printing
        '''
        
        results = []
        
        for preset in presets:
            
            ov = OrderedDict()
            
            iops_guarantee = preset.iops_guarantee
            
            if iops_guarantee == 0:
                iops_guarantee = "None"
                
            iops_limit = preset.iops_limit
            
            if iops_limit == 0:
                iops_limit = "Forever"
            
            ov["ID"] = preset.id
            ov["Name"] = preset.name
            ov["Priority"] = preset.priority
            ov["IOPs Guarantee"] = iops_guarantee
            ov["IOPs Limit"] = iops_limit
            
            results.append( ov )
            
        return results
    
    @staticmethod
    def prep_qos_for_table( qos ):
        '''
        Makes a table for the QOS object
        '''
        
        ov = OrderedDict()
        
        preset_id = qos.preset_id
        
        if ( preset_id == None ):
            preset_id = "None"
        
        if ( preset_id != "None" ):
            ov["Preset ID"] = preset_id
            
        ov["Priority"] = qos.priority
        ov["IOPs Guarantee"] = qos.iops_min
        ov["IOPs Limit"] = qos.iops_max
        
        results = [ov]
        
        return results
            
    @staticmethod
    def prep_safeguard_presets(presets):
        '''
        Prep a list of safeguard presets for tabular printing

        Returns
        -------
        List[string]
        '''
        results = []
        for preset in presets:

            ov = OrderedDict()

            if preset.id != None:
                ov["ID"] = preset.id

            if ( preset.name != None and preset.name != "" ):
                ov["Name"] = preset.name

            ov["Recurrence Rule"] = RecurrenceRuleConverter.to_json( preset.recurrence_rule )

            results.append( ov )

        return results

    @staticmethod
    def prep_subscriptions_for_table(subscriptions):
        '''
        Converts each subscription to an ordered dictionary for tabular display.

        Parameters
        ----------
        :type subscriptions: list(``model.volume.Subscription``)
        :param subscriptions: List of subscription objects

        Returns
        -------
        :type list(dict)
        '''
        results = []

        for subscription in subscriptions:

            ov = OrderedDict()

            ov["ID"] = subscription.digest
            ov["Name"] = subscription.name
            ov["Volume ID"] = subscription.volume_id
            ov["Recurrence Rule"] = RecurrenceRuleConverter.to_json( subscription.recurrence_rule )
            ov["Named Credential"] = subscription.named_credential.name

            results.append( ov )

        return results

    @staticmethod
    def prep_users_for_table(users):
        '''
        Put the list of users in a nice readable tabular format
        '''
        
        d_users = []
        
        for user in users:
            ov = OrderedDict()
            
            ov["ID"] = user.id
            ov["Username"] = user.name
            
            d_users.append( ov )
            
        return d_users
        
    @staticmethod
    def prep_tenants_for_table(tenants):
        '''
        Scrub the tenant objects for a readable tabular format
        '''
        
        d_tenants = []
        
        for tenant in tenants:
            ov = OrderedDict()
            
            ov["ID"] = tenant.id
            ov["Name"] = tenant.name
            d_tenants.append( ov )
            
        return d_tenants
    
    @staticmethod
    def prep_system_health_for_table(health):
        
#         if not isinstance(health, SystemHealth):
#             raise TypeError()
        
        ov = OrderedDict()
        
        cap_record = None
        service_record = None
        fb_record = None
        
        for record in health.health_records:
            if record.category == HealthCategory.CAPACITY:
                cap_record = record
            elif record.category == HealthCategory.SERVICES:
                service_record = record
            elif record.category == HealthCategory.FIREBREAK:
                fb_record = record
                
        
        ov["Overall"] = health.overall_health
        ov["Capacity"] = cap_record.state
        ov["Services"] = service_record.state
        ov["Firebreak"] = fb_record.state
        
        results =[ov]
        
        return results

    @staticmethod
    def prep_exports_for_table( session, exports ):
        '''
        Prep a list of exported volume records for tabular printing.

        Returns
        -------
        list(OrderedDict)
        '''
        results = []

        for exported_volume in exports:

            ov = OrderedDict()
            creation_time = time.localtime( long(exported_volume.creation_time) )
            creation_time = time.strftime( "%c", creation_time )
            ov["Name"] = exported_volume.obj_prefix_key
            ov["Type"] = exported_volume.source_volume_type
            ov["Source Volume Name"] = exported_volume.source_volume_name
            ov["Export Time"] = creation_time
            ov["Blob Count"] = exported_volume.blob_count
            results.append( ov )

        return results

    @staticmethod
    def prep_zone_for_table(session, response):
        '''
        Take the zone response and make it consumable for a table
        '''

        resultList = []

        for zone in response:

            ov = OrderedDict()

            ov["ID"] = zone.zid
            ov["Name"] = zone.name
            ov["Type"] = zone.ztype
            ov["State"] = zone.state
            ov["VIP"] = zone.zvip
            ov["AM1"] = zone.amList[0]
            ov["AM2"] = zone.amList[1]

            resultList.append(ov)
            # end for loop

        return resultList

