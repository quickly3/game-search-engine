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
        $this->source = [];
    }

    public function search($params){
        return $this->client->search($params);
    }

    public function source($source){
        $this->source = $source;
        return $this;
    }

    public function query($query){

        $params = [
            "index" => $this->index,
            "type" => $this->index_type,
            "body"=>[
                "query"=> $query
            ]
        ];
        
        $this->setSource();
        $this->setReqRes($params);
        
        return $this;
    }

    private function setSource(){
        if(!empty($this->source)){
            $params['body']['_source'] = $this->source;
        }
    }

    private function setReqRes($params){
        $this->reqRes = $this->client->search($params);
    }

    public function match_all(){
        $params = [
            "index" => $this->index,
            "type" => $this->index_type,
            "body"=>[
                "query"=> [  "match_all" => (object)[]]
            ]
        ];        
        $this->setSource();
        $this->setReqRes($params);
        
        return $this;
    }

    public function getRes(){
        $hits = $this->reqRes["hits"]["hits"];
        return $hits;
    }

    public function getIdRes(){
        $res = [];
        $hits = $this->reqRes["hits"]["hits"];
        if(!empty($hits)){
            foreach ($hits as $key => $item) {
                $source = $item['_source'];
                $source['_id'] = $item['_id'];
                $res[] = $source;
            }
        }
        return $res;
    }
}
