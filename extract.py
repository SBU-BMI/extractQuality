#!/usr/local/bin/python3
from pymongo import MongoClient
from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry.polygon import LinearRing
from shapely.geometry import Polygon
from bson import json_util 
import numpy as np
import time
import pprint
import json 
import csv
import sys
import os
import shutil
import subprocess
import pipes

if __name__ == '__main__':
    # Check arguments and display usage
    if len(sys.argv)<1:
        print("usage:python extract.py case_id exec_id")
        exit()
    caseid = sys.argv[1]
    execid = sys.argv[2]
    regionsToDownload = []
    start_time = time.time()
    my_home="."
    out_dir  =os.path.join(my_home, 'composite_results/')
    db_host="hedwig.bmi.stonybrook.edu"
    db_port="27017"
    #multiple process number
    max_workers=16
    pp = pprint.PrettyPrinter(indent=4)

    client = MongoClient('mongodb://'+db_host+':'+db_port+'/')
    db = client.quip
    objects = db.objects
    metadata = db.metadata
    heatmapsByCidQuery = {'object_type': 'heatmap_quality','provenance.analysis.execution_id': execid}
    muByCidQuery = {'object_type': 'marking','provenance.image.case_id': caseid, 'properties.annotations.mark_eid': execid}
    qheatmaps = objects.find(heatmapsByCidQuery)
    markups = objects.find(muByCidQuery)
    for heatmap in qheatmaps:
        pp.pprint(heatmap)
    print("-------------------------------------")
    for item in markups:
        pp.pprint(item['provenance'])

    # analysis_list_csv = os.path.join(my_home, input_file);
    # if not os.path.isfile(analysis_list_csv):
    #   print "caseid_perfix_algorithm file is not available."
    #   exit();
    #
    # print '--- read master CSV file ---- ';
    # index=0;
    # analysis_list=[];
    # with open(analysis_list_csv, 'r') as my_file:
    #   reader = csv.reader(my_file, delimiter=',')
    #   my_list = list(reader);
    #   for each_row in my_list:
    #     tmp_analysis_list=[[],[],[]];
    #     tmp_analysis_list[0]= each_row[0];
    #     tmp_analysis_list[1]= each_row[1];
    #     tmp_analysis_list[2]= each_row[2];
    #     analysis_list.append(tmp_analysis_list);
    # print "total rows from master csv file is %d " % len(analysis_list) ;
    #
    # def getPrefix(case_id,algorithm):
    #   prefix="";
    #   for tmp in analysis_list:
    #     case_id_row=tmp[0];
    #     prefix_row=tmp[1];
    #     algorithm_row=tmp[2];
    #     if (case_id_row == case_id and algorithm_row == algorithm):
    #         prefix =prefix_row;
    #         break
    #   return  prefix;
    #
    # excluded_list=['joseph.balsamo','tahsin.kurc','tigerfan7495','joelhsaltz','tammy.diprima','siwen.statistics']
    # process_list =[];
    # for case_id in case_id_list:
    #   subject_id=case_id;
    #   user_list =[];
    #   tmp_process_list_item=[[],[],[],[],[]];
    #   prefixs_algorithm=[];
    #   polygon_algorithm=[[0 for y in xrange(2)] for x in xrange(1000)];
    #   for user_composite_input in  metadata.find({"image.case_id":case_id,
    #                    "provenance.analysis_execution_id":{'$regex':'_composite_input'}},
    #                    {"provenance.analysis_execution_id":1}):
    #     tmp=user_composite_input["provenance"]["analysis_execution_id"];
    #     tmp_user =tmp.split('_')[0];
    #     user_list.append(tmp_user);
    #   for exclued_user in excluded_list:
    #     if exclued_user in user_list:
    #       user_list.remove(exclued_user);
    #   user_count=len(user_list);
    #   if user_count >1:
    #     user = user_list[0];# get first user
    #     if ( case_id == "17033063"):
    #       tmp_process_list_item[0]=case_id;
    #       tmp_process_list_item[1]='lillian.pao';
    #       #process_list.append(tmp_process_list_item);
    #     elif ( case_id == "BC_056_0_1"):
    #       tmp_process_list_item[0]=case_id;
    #       tmp_process_list_item[1]='areeha.batool';
    #       #process_list.append(tmp_process_list_item);
    #     elif ( case_id == "BC_061_0_2"):
    #       tmp_process_list_item[0]=case_id;
    #       tmp_process_list_item[1]='lillian.pao';
    #       #process_list.append(tmp_process_list_item);
    #     elif ( case_id == "BC_065_0_2"):
    #       tmp_process_list_item[0]=case_id;
    #       tmp_process_list_item[1]='epshita.das';
    #       #process_list.append(tmp_process_list_item);
    #     elif ( case_id == "PC_227_2_1"):
    #       tmp_process_list_item[0]=case_id;
    #       tmp_process_list_item[1]='areeha.batool';
    #       #process_list.append(tmp_process_list_item);
    #     else:# assign first user
    #       tmp_process_list_item[0]=case_id;
    #       tmp_process_list_item[1]=user;
    #       #process_list.append(tmp_process_list_item);
    #   elif user_count<1:
    #     #print " ------ case_id:  "+case_id + "---------------------------";
    #     #print "no user for this case id!!!";
    #     tmp_process_list_item[0]=case_id;
    #     tmp_process_list_item[1]="";
    #   else:#only one user
    #     tmp_process_list_item[0]=case_id;
    #     tmp_process_list_item[1]=user_list[0];
    #
    #   if (user_count > 0):#user is available
    #     execution_id=tmp_process_list_item[1] +"_composite_input";
    #     tmp_algorithm_list=[];
    #     annotation_count=0;
    #     print '----- get human markups for this image and this user -----';
    #     for annotation in objects.find({"provenance.image.case_id":case_id,
    #                                   "provenance.image.subject_id":subject_id,
    #                                   "provenance.analysis.execution_id": execution_id
    #           },{"_id":0,"geometry.coordinates":1,"algorithm":1}):
    #       polygon=annotation["geometry"]["coordinates"][0];
    #       algorithm=annotation["algorithm"];
    #       tmp_algorithm_list.append(algorithm);
    #       x=polygon[0][0];
    #       y=polygon[0][1];
    #       if(x<0.0 or x>1.0):
    #         continue;
    #       if(y<0.0 or y>1.0):
    #         continue;
    #       polygon_algorithm[annotation_count][0]=algorithm;
    #       polygon_algorithm[annotation_count][1]=polygon;
    #       annotation_count+=1;
    #     print 'total annotation number is %d' % annotation_count;
    #     total_annotation_count = annotation_count;
    #     algorithm_list = sorted(set(tmp_algorithm_list));
    #     for algorithm in algorithm_list:
    #       prefix=getPrefix(case_id,algorithm);
    #       tmp_prefixs_algorithm =[[],[]];
    #       tmp_prefixs_algorithm[0]=prefix;
    #       tmp_prefixs_algorithm[1]=algorithm;
    #       prefixs_algorithm.append(tmp_prefixs_algorithm);
    #     tmp_process_list_item[2]=prefixs_algorithm;
    #     tmp_process_list_item[3]=total_annotation_count;
    #     tmp_process_list_item[4]=polygon_algorithm;
    #     process_list.append(tmp_process_list_item);
    # print "final user and case_id combination is  %d " % len(process_list) ;
    #
    # print " --- ----  copy all results files from storage node ----";
    # for tmp_user_case_id in  process_list:
    #   case_id=tmp_user_case_id[0];
    #   user=tmp_user_case_id[1];
    #   prefixs_algorithm=tmp_user_case_id[2];
    #   print " --- case_id  and user are %s / %s  -------" % (case_id,user);
    #   for tmp_item in prefixs_algorithm:
    #     prefix = tmp_item[0];
    #     algorithm = tmp_item[1];
    #     print "--- algorithm is " +algorithm + "------"
    #     local_img_folder = os.path.join(main_dir, case_id);
    #     local_folder = os.path.join(local_img_folder, prefix);
    #     if not os.path.exists(local_folder):
    #       print '%s folder do not exist, then create it.' % local_folder;
    #       os.makedirs(local_folder);
    #     if os.path.isdir(local_folder) and len(os.listdir(local_folder)) > 0:
    #       print " all csv and json files have been copied from data node.";
    #     else:
    #       print " No  csv and json files have been copied from data node yet.";
    #       continue;
    #
    # print " --- ----  start the loop of  case_id  and user combination ----";
    # for user_case_id in  process_list:
    #   loop_index=process_list.index(user_case_id);
    #   case_id=user_case_id[0];
    #   subject_id=case_id;
    #   user=user_case_id[1];
    #   prefixs_algorithm=user_case_id[2];
    #   total_annotation_count=user_case_id[3];
    #   polygon_algorithm=user_case_id[4];
    #   new_execution_id=user +"_composite_dataset";
    #
    #   print '-- find all annotations NOT within another annotation  -- ';
    #   polygon_algorithm_final=[[0 for y in xrange(3)] for x in xrange(1000)];
    #   index3=0
    #   for index1 in range(0, total_annotation_count):
    #     algorithm = polygon_algorithm[index1][0];
    #     annotation = polygon_algorithm[index1][1];
    #     tmp_poly=[tuple(i) for i in annotation];
    #     annotation_polygon1 = Polygon(tmp_poly);
    #     annotation_polygon_1 = annotation_polygon1.buffer(0);
    #     polygonBound= annotation_polygon_1.bounds;
    #     array_size=len(annotation);
    #     print '-----------------------------------------------------------------';
    #     print "annotation index %d and annotation point size %d" % (index1, array_size) ;
    #     is_within=False;
    #     for index2 in range(0, total_annotation_count):
    #       annotation2 = polygon_algorithm[index2][1];
    #       tmp_poly2=[tuple(j) for j in annotation2];
    #       annotation_polygon2 = Polygon(tmp_poly2);
    #       annotation_polygon_2 = annotation_polygon2.buffer(0);
    #       if index1 <> index2 and not annotation_polygon_1.equals(annotation_polygon_2):
    #         if (annotation_polygon_1.within(annotation_polygon_2)):
    #           is_within=True;
    #           polygonBound2= annotation_polygon_2.bounds;
    #           array_size2=len(annotation2);
    #           break
    #     if not is_within:
    #       print 'add annotation of index %d' % index1;
    #       polygon_algorithm_final[index3][0]=algorithm;
    #       polygon_algorithm_final[index3][1]=annotation;
    #       polygon_algorithm_final[index3][2]=index1;
    #       index3+=1;
    #   print 'final annotation number is %d' % index3;
    #   final_total_annotation_count=index3;
    #   #print polygon_algorithm_final;
    #
    #   print '------ get all tiles as polygon ------ ';
    #   title_polygon_algorithm_final=[[0 for y in xrange(3)] for x in xrange(10000)];
    #   print 'total_algorithms is %s' % len(prefixs_algorithm);
    #   for index1 in range (0,len(prefixs_algorithm)):
    #     prefix = prefixs_algorithm[index1][0];
    #     algorithm = prefixs_algorithm[index1][1];
    #     img_folder = os.path.join(main_dir, case_id);
    #     algorithm_folder = os.path.join(img_folder, prefix);
    #     #print '----------------------------------------------------';
    #     print 'algorithm data files location %s' % algorithm_folder;
    #     if os.path.isdir(algorithm_folder) and len(os.listdir(algorithm_folder)) > 0:
    #       json_filename_list = [f for f in os.listdir(algorithm_folder) if f.endswith('.json')] ;
    #       print 'there are %d json files in this folder.' % len(json_filename_list);
    #       tmp_title_polygon=[];
    #       for json_filename in json_filename_list:
    #         with open(os.path.join(algorithm_folder, json_filename)) as f:
    #           data = json.load(f);
    #           analysis_id=data["analysis_id"];
    #           image_width=data["image_width"];
    #           image_height=data["image_height"];
    #           tile_minx=data["tile_minx"];
    #           tile_miny=data["tile_miny"];
    #           tile_width=data["tile_width"];
    #           tile_height=data["tile_height"];
    #           title_polygon=[[float(tile_minx)/float(image_width),float(tile_miny)/float(image_height)],[float(tile_minx+tile_width)/float(image_width),float(tile_miny)/float(image_height)],[float(tile_minx+tile_width)/float(image_width),float(tile_miny+tile_height)/float(image_height)],[float(tile_minx)/float(image_width),float(tile_miny+tile_height)/float(image_height)],[float(tile_minx)/float(image_width),float(tile_miny)/float(image_height)]];
    #           tmp_list=[[],[]];
    #           tmp_list[0]=json_filename;
    #           tmp_list[1]=title_polygon;
    #           tmp_title_polygon.append(tmp_list);
    #       print 'tmp title polygon length %d' % len(tmp_title_polygon);
    #     title_polygon_algorithm_final[index1][0]=prefix;
    #     title_polygon_algorithm_final[index1][1]=algorithm;
    #     title_polygon_algorithm_final[index1][2]=tmp_title_polygon ;
    #     print 'index1 is %d '% index1;
    #     print  'there are %d titles in folder %s .' % (len(title_polygon_algorithm_final[index1][2]) ,algorithm_folder);
    #
    #
    #   # ---- process_one_tile function  ---
    #   def process_one_tile(title_index,algorithm,title_array,algorithm_folder_in,algorithm_folder_out):
    #     is_intersects=False;
    #     is_within=False;
    #     json_filename=title_array[0];
    #     csv_filename=json_filename.replace('algmeta.json','features.csv');
    #     tmp_polygon=title_array[1];
    #     print  '--- current title_index is %d' % title_index;
    #     annotation_title_intersect_list =[];
    #     for index2 in range (0,final_total_annotation_count):
    #       algorithm2=polygon_algorithm_final[index2][0];
    #       if (algorithm == algorithm2):
    #         tmp_poly=[tuple(i) for i in tmp_polygon];
    #         title_polygon = Polygon(tmp_poly);
    #         title_polygon = title_polygon.buffer(0);
    #         annotation=polygon_algorithm_final[index2][1];
    #         tmp_poly2=[tuple(j) for j in annotation];
    #         annotation_polygon = Polygon(tmp_poly2);
    #         annotation_polygon = annotation_polygon.buffer(0);
    #         if (title_polygon.within(annotation_polygon)):
    #           is_within=True;
    #           break;
    #         elif (title_polygon.intersects(annotation_polygon)):
    #           is_intersects=True;
    #           annotation_title_intersect_list.append(annotation);
    #
    #     if(is_within or is_intersects):
    #       if is_intersects:
    #         print '       title %d intersects with human markup %d' % (title_index,index2);
    #       if is_within:
    #         print '       title %d is within with human markup %d' % (title_index,index2);
    #       print '       json_filename is %s' % json_filename;
    #       print '       csv_filename is %s' % csv_filename;
    #       json_source_file = os.path.join(algorithm_folder_in, json_filename);
    #       csv_source_file = os.path.join(algorithm_folder_in, csv_filename);
    #       json_dest_file = os.path.join(algorithm_folder_out, json_filename);
    #       csv_dest_file = os.path.join(algorithm_folder_out, csv_filename);
    #       if not os.path.isfile(json_dest_file):
    #         shutil.copy2(json_source_file,json_dest_file) ;
    #       if not os.path.isfile(csv_dest_file):
    #         shutil.copy2(csv_source_file,csv_dest_file) ;
    #       #update analysis_id info in json file
    #       with open(json_dest_file, 'r') as f:
    #        json_data = json.load(f)
    #        analysis_id = json_data['analysis_id'];
    #        image_width=json_data["image_width"];
    #        image_height=json_data["image_height"];
    #        json_data['analysis_id'] = new_execution_id;
    #        json_data['analysis_desc'] = analysis_id;
    #       with open(json_dest_file, 'w') as f2:
    #         f2.write(json.dumps(json_data));
    #
    #     if is_intersects:
    #       #print 'intersect annotation number is %d.' % len(annotation_title_intersect_list);
    #       json_dest_file = os.path.join(algorithm_folder_out, json_filename);
    #       csv_dest_file = os.path.join(algorithm_folder_out, csv_filename);
    #       my_tem_file ='tmp_file_'+ str(title_index)+'.csv';
    #       tmp_file = os.path.join(algorithm_folder_out, my_tem_file);
    #       with open(csv_dest_file, 'rb') as csv_read, open(tmp_file, 'wb') as csv_write:
    #         reader = csv.reader(csv_read);
    #         headers = reader.next();
    #         #write header to tmp file
    #         csv_writer = csv.writer(csv_write);
    #         csv_writer.writerow(headers);
    #         polygon_index= headers.index('Polygon');
    #         for row in reader:
    #           current_polygon=row[polygon_index] ;
    #           new_polygon=[];
    #           tmp_str=str(current_polygon);
    #           tmp_str=tmp_str.replace('[','');
    #           tmp_str=tmp_str.replace(']','');
    #           split_str=tmp_str.split(':');
    #           for i in range(0, len(split_str)-1, 2):
    #             point=[float(split_str[i])/float(image_width),float(split_str[i+1])/float(image_height)];
    #             new_polygon.append(point);
    #           tmp_poly=[tuple(i) for i in new_polygon];
    #           computer_polygon = Polygon(tmp_poly);
    #           computer_polygon = computer_polygon.buffer(0);
    #           has_intersects=False;
    #           for annotation in annotation_title_intersect_list:
    #             tmp_poly2=[tuple(j) for j in annotation];
    #             annotation_polygon = Polygon(tmp_poly2);
    #             annotation_polygon = annotation_polygon.buffer(0);
    #             if (computer_polygon.intersects(annotation_polygon)):
    #               has_intersects=True;
    #               break;
    #           #write each row to the tmp csv file
    #           if has_intersects:
    #             csv_writer.writerow(row) ;
    #       shutil.move(tmp_file,csv_dest_file);
    #       print 'change tem file of %s  to file %s' % (tmp_file,csv_dest_file);
    #   # ---- end of process_one_tile function  ---
    #
    #   print" ---- find all title intersect with human markups ---- ";
    #   start_time2 = time.time();
    #   for index1 in range (0,len(prefixs_algorithm)):
    #     prefix=title_polygon_algorithm_final[index1][0];
    #     algorithm=title_polygon_algorithm_final[index1][1];
    #     tmp_title_polygon_list=title_polygon_algorithm_final[index1][2];
    #     img_folder = os.path.join(main_dir, case_id);
    #     algorithm_folder = os.path.join(img_folder, prefix);
    #     out_folder = os.path.join(out_dir, case_id);
    #     out_algorithm_folder = os.path.join(out_folder, prefix);
    #     if not os.path.exists(out_algorithm_folder):
    #       os.makedirs(out_algorithm_folder);
    #     print " --------- deal with algorithm %s -------------- " % algorithm;
    #     title_index=0;
    #     #--- apply multiple process method ---
    #     with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
    #       for tmp_title_polygon in tmp_title_polygon_list:
    #         executor.submit(process_one_tile, title_index,algorithm,tmp_title_polygon,algorithm_folder,out_algorithm_folder);
    #         title_index+=1;
    # #end of  process_list
    # print " --- ----  End of loop for case_id and user combination ----";
    #
    # print "--- end of program --- ";
    elapsed_time = time.time() - start_time  
    print ("total time to run whole program is "+str(elapsed_time/60.00)+ ' minutes.')
    exit();