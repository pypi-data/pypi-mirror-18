#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of OTC Tool released under MIT license.
# Copyright (C) 2016 T-systems Kurt Garloff, Zsolt Nagy


from otcclient.core.OtcConfig import OtcConfig 
from otcclient.utils import utils_http

from otcclient.core.otcpluginbase import otcpluginbase
from otcclient.core.pluginmanager import getplugin

import json
from otcclient.plugins.ecs import ecs

    
class mrs(otcpluginbase):
    ar = {}    
    
    @staticmethod
    def otcOutputHandler(): 
        return getplugin(OtcConfig.OUTPUT_FORMAT)
 
    def otctype(self):
        return "func" 

    @staticmethod
    def update_image_metadata():
        if not (OtcConfig.IMAGENAME is None):
            ecs.convertIMAGENameToId()
        mrs.create_image_metadata()

    @staticmethod
    def create_image_metadata():
                
        # image id filled until now 
        url = "https://" + OtcConfig.DEFAULT_HOST + "/v2/images" 
        REQ_CREATE_META_IMAGE = "{    \"__os_version\": \"" + OtcConfig.OS_VERSION + "\",\"container_format\": \"" + OtcConfig.CONTAINTER_FORMAT +  "\",\"disk_format\": \"" + OtcConfig.DISK_FORMAT + "\",    \"min_disk\": " +  OtcConfig.MIN_DISK + ",\"min_ram\": " + OtcConfig.MIN_RAM + ",\"name\": \"" + OtcConfig.IMAGENAME + "\",\"tags\": [\"" + OtcConfig.TAG_LIST + "\",\"image\"],\"visibility\": \"" + OtcConfig.IMAGE_VISIBILITY + "\",\"protected\": " + OtcConfig.PROTECTED + "}"    
        ret = utils_http.post(url, REQ_CREATE_META_IMAGE)        
        mrs.otcOutputHandler().print_output(ret, mainkey="") 

        OtcConfig.IMAGE_ID = json.loads(ret)["id"]
        
        if OtcConfig.IMAGE_ID is None: 
            raise RuntimeError("Image not created! " + ret)

        return ret

    @staticmethod
    def register_image():
        if not (OtcConfig.IMAGENAME is None):
            ecs.convertIMAGENameToId()
        
        if OtcConfig.IMAGE_ID is None:
            # error handling 
            raise RuntimeError("Please define image id!")
        
        # image id filled until now 
        url = "https://" + OtcConfig.DEFAULT_HOST + "/v2/images/" + OtcConfig.IMAGE_ID + "/file"
        REQ_REG_IMAGE = "{\"image_url\":\"" + OtcConfig.IMAGE_URL + "\" }"
        ret = utils_http.put(url, REQ_REG_IMAGE)
        if len(ret) != 0: 
            print ("Image registration error!" + ret) 
        return ret

    @staticmethod
    def describe_clusters():
        #url = "https://" + OtcConfig.DEFAULT_HOST + "/v1/" + OtcConfig.PROJECT_ID +  "/bigdata/clusters"
        url = "https://" + OtcConfig.DEFAULT_HOST + "/bigdata/api/v1/clusters?pageSize=10&currentPage=1&clusterState=existing"
        
        #if not OtcConfig.CLUSTER is None:
        #    mrs.convertCLUSTERNameToId() 

        if OtcConfig.CLUSTER_ID is None: 
            ret = utils_http.get(url)
            print (url)
            print (ret)        
            ecs.otcOutputHandler().print_output(ret, mainkey = "clusters", listkey={"id", "name"})
        else:            
            ret = utils_http.get(url + '/' + OtcConfig.INSTANCE_ID )        
            maindata = json.loads(ret)
            if "itemNotFound" in  maindata:
                raise RuntimeError("Not found!")                      
            ecs.otcOutputHandler().print_output(ret,mainkey="server") 
        return ret


    @staticmethod
    def create_image():        
        mrs.create_image_metadata()        
        ret = mrs.register_image()        
        return ret
