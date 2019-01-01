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


class GameController extends Controller
{
    public function getList(Request $request){

        $db = $request->input("db","mysql");

        $es = new ElasticModel("games","games");
        $query = [  "match_all" => (object)[]];
        $query_string = "name:英雄";

        $data = $es->source(["name","version"])->query_string($query_string,"*")->paginate(10);

        // $data = DB::table("Game")->paginate(20);

        return response()->json($data);
    }

    public function test(Request $request){
        $es = new ElasticModel("games","game");
        $query = [  "match_all" => (object)[]];
        $query_string = "name:英雄";
        $data = $es->source(["name","version"])->query_string($query_string,"*")->paginate(10);

    	return response()->json($data); 
    }
}
