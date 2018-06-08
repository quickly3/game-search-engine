<?php

namespace App\Http\Controllers;

use Solarium;

class HomeController extends Controller
{

    public function get_home_list(){

        $config = array(
            'endpoint' => array(
                'localhost' => array(
                    'host' => "127.0.0.1",
                    'port' => "8983",
                    'path' => '/solr/master-graph-2/',
                )
            )
        );

        // create a client instance
        $client = new Solarium\Client($config);

        // get a select query instance
        $query = $client->createSelect();
        $query->setQuery("DocumentType:Candidate");
        $query->setFields(['*']);
        // this executes the query and returns the result
        $resultset = $client->execute($query);

        // display the total number of documents found by solr

        // show documents using the resultset iterator
        $list = array();
        foreach ($resultset as $document) {
            $item = new \stdClass();
            // the documents are also iterable, to get all fields
            foreach ($document as $field => $value) {
                if (is_array($value)) {
                    $arr = array();
                    foreach ($value as $v){
                        if(json_decode($v))
                            array_push($arr, json_decode($v));
                        else
                            array_push($arr, $v);
                    }
                    $value = $arr;
                }
                $item->$field = $value;
            }
            array_push($list, $item);
        }


        return response()->json($list);
    }
}
