<?php

namespace App\Console\Commands;

use App\User;
use Illuminate\Console\Command;
use DB;
use App\Model\Elastic\ElasticModel;
use DateTime;

class EscnToEs extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     * @translator laravelacademy.org
     */
    protected $signature = 'EscnToEs';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Send drip e-mails to a user';

    /**
     * The drip e-mail service.
     *
     */
    protected $drip;

    /**
     * Create a new command instance.
     *
     */
    public function __construct()
    {
        parent::__construct();

    }

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {

        $start = 0;
        $row = 100;

        $es = new ElasticModel("escn","escn");

        $count = DB::table("EsDailyItem")->where("state","init")->count();
        $current = 0;

        while($datas = DB::table("EsDailyItem")->where("state","init")->select()->orderBy("id")->limit(100)->get()){
            $ids = [];
            foreach ($datas as $key => $data) {
                $ids[] = $data->id;

                $params = [
                    "index" => "escn",
                    "type" => "escn",
                    "body" =>  $data 
                ];

                $data = $es->client->index($params);

            }

            $current += count($datas);

            DB::table("EsDailyItem")->whereIn("id",$ids)->update(["state"=>"completed"]);

            $this->info("{$current}/{$count}");

            if(count($datas) == 0 ){
                return false;
            }            
        }
    }
}