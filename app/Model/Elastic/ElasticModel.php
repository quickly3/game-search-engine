<?php

namespace App\Model\Elastic;
use Elasticsearch\ClientBuilder;

class ElasticModel  
{
    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function __construct($index_name,$type)
    {
        $this->connect();
        $this->index = $this->index_maped($index_name);
        $this->index_type = $type;

    }

    public function index_maped($index_name){
        $map = [
            "games" => "games"
        ];

        return isset($map[$index_name])?$map[$index_name]:$index_name;
    }


    /**
     * Register any application services.
     *
     * @return void
     */
    public function connect()
    {
        $hosts = [];
        $main_host = getenv("ES_HOST").":".getenv("ES_PORT");
        $hosts[] = $main_host;

        $clientBuilder = ClientBuilder::create();   // Instantiate a new ClientBuilder
        $clientBuilder->setHosts($hosts);           // Set the hosts
        $this->client = $clientBuilder->build(); 
    }

    public function search($params){
        return $this->client->search($params);
    }


    public function query($query){

        $params = [
            "index" => $this->index,
            "type" => $this->index_type,
            "body"=>[
                "query"=> $query
            ]
        ];
        $res = $this->client->search($params);
        return $res['hits'];
    }
}
