<?php

namespace App\Services;

use App\Model\Elastic\ElasticModel;

class EscnService 
{
	public static function genWordsCloud(){
		$cloud_words = [];

        $es = new ElasticModel("escn","escn");
        $data = [
            "aggs"=>[
                "title_words_cloud"=>[
                    "terms" => [
                        "field" => "title",
                        "size" => 100
                    ]
                ]
            ],
            "size"=>0
        ];

        $params = [
            "index" => "escn",
            "type" => "escn",
            "body" =>  $data 
        ];

        $data = $es->client->search($params);
        $resp = (object)$data;
        $cloud_words = $resp->aggregations['title_words_cloud']['buckets'];

        $cloud_words = array_map(function($item){
            return (object)$item;
        }, $cloud_words);


        $stop_words = [
            "elasticsearch","使用","elastic","es","21","2018","如何","基于","中国","一个","进行","发售",
            "开始","门票","上海","合作","请和","赞助","报名","接受","看看","了解","day"
        ];

        $cloud_words = array_filter($cloud_words,function($item) use ($stop_words){

            $matched = true;

            if(mb_strlen($item->key) == 1){
                $matched = false;
            }

            if(in_array($item->key,$stop_words)){
                $matched = false;
            }

            return $matched;
        });

        $cloud_words = array_merge($cloud_words,[]);	
        return $cloud_words;	
	}
}
