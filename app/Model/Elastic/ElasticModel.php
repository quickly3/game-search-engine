<?php

namespace App\Model\Elastic;
use Elasticsearch\ClientBuilder;
use Request;

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
        $this->page = 1;
        $this->size = 10;
        $this->from = 0;
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

    public function query_string($keyword,$fields){
        $params = [
            "index" => $this->index,
            "type" => $this->index_type,
            "body"=>[
                "query"=> [
                    "query_string" => [
                        "default_field" => $fields,
                        "query" => $keyword
                    ]
                ]
            ]
        ];
        $this->request_body = $params;
        return $this;
    }

    public function size($size){
        $this->request_body["body"]["size"] = $size;
        return $this;
    }



    public function from($from){
        $this->request_body["body"]["from"] = $from;
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
        $this->request_body = $params;
        $this->setSource();
        $this->setReqRes();
        
        return $this;
    }

    public function paginate($size){
        $page = (int)Request::input("page",1);
        $from = ($page - 1) * $this->size;
        $this->request_body["body"]["size"] = $size;
        $this->request_body["body"]["from"] = $from ;
        $this->setReqRes();
        $res = [];

        
        $res['current_page'] = $page;
        $res['total'] = $this->reqRes['hits']['total'];

        $res['last_page'] = ceil($res['total']/$size);
        $res['from'] = $from;
        $res['to'] = $from + $size;
        $res['per_page'] = $size;


        // $res['first_page_url'] = $page;
        // $res['last_page_url'] = $page;
        // $res['next_page_url'] = $page;
        // $res['prev_page_url'] = $page;
        // $res['path'] = $page;

        $res['data'] = $this->getIdRes();
        return $res;
    }

    private function setSource(){
        if(!empty($this->source)){
            $params['body']['_source'] = $this->source;
        }
    }

    private function setReqRes(){
        $this->reqRes = $this->client->search($this->request_body);
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
