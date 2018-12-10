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

        $db = $request->input($db,"mysql");

        $data = DB::table("Game")->paginate(20);

        return response()->json($data);
    }

    public function test(Request $request){
        $es = new ElasticModel("games","game");
        $query = [  "match_phrase" => [
                        "game_tags_string" => "3D画面"
                    ]
                 ];
        $res = $es->query($query);
        dump($res);die();
    	$data = [];
    	return response()->json($data); 
    }
}
