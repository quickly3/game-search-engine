<?php

namespace App\Http\Controllers;

use App\Common\Model\MySQLModel\Location;
use App\Common\Model\MySQLModel\NewLocation;
use App\Common\Services\Traits\AddressCityNameAliasTrait;
use App\Http\Controllers\Controller;
use App\Http\Requests;
use DB;
use Illuminate\Http\Request;
use App\Model\Elastic\ElasticModel;


class FanjuController extends Controller
{
    public function getList(Request $request){

        $keywords = $request->input("keywords","");
        $search_type = trim($request->input("search_type",""));

        $es = new ElasticModel("fanju","fanju");

        if($search_type == "simple"){
            $data = $es->source(["fanju_title","version"]);
            if(trim($keywords) == ""){
                $keywords = "''";
            }
        }else{
            $data = $es;
            if(trim($keywords) == ""){
                $keywords = "*";
            }
        }

        $orders = [
            "_score"=>"desc",
            "pub_date"=>"desc"
        ];

        $query_string = "fanju_title_text:{$keywords}";

        $data->orderBy($orders);

        $data = $data->query_string($query_string,"*")->paginate(10);

        $data['query_string'] = $query_string;

        return response()->json($data);
    }

    public function test(Request $request){
        $es = new ElasticModel("games","game");
        $query = [  "match_all" => (object)[]];
        $query_string = "name:英雄";
        $data = $es->source(["name","version"])->query_string($query_string,"*")->paginate(10);

    	return response()->json($data); 
    }

    public function getGameDataById(Request $request){
        $id = $request->input("id","");

        $es = new ElasticModel("games","games");
        $query = [  "match_all" => (object)[]];
        $query_string = "name:英雄";
        $data = $es->source(["name","version"])->getById($id,"*");

    	return response()->json($data); 
    }


}
