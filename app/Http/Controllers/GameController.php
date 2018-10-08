<?php

namespace App\Http\Controllers;

use App\Common\Model\MySQLModel\Location;
use App\Common\Model\MySQLModel\NewLocation;
use App\Common\Services\Traits\AddressCityNameAliasTrait;
use App\Http\Controllers\Controller;
use App\Http\Requests;
use DB;
use Illuminate\Http\Request;
use Elasticsearch\ClientBuilder;

class GameController extends Controller
{
    public function getList(Request $request){

        $data = DB::table("Game")->paginate(20);

        return response()->json($data);
    }

    public function test(Request $request){

    	

    	$data = [];
    	return response()->json($data); 
    }
}
