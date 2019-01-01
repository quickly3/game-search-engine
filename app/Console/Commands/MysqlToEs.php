<?php

namespace App\Console\Commands;

use App\User;
use Illuminate\Console\Command;
use DB;
use App\Model\Elastic\ElasticModel;
use DateTime;

class MysqlToEs extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     * @translator laravelacademy.org
     */
    protected $signature = 'MysqlToEs';

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

        $es = new ElasticModel("games","game");
        $params = [
            "index" => "bank",
            "type" => "account",
        ];

        $count = DB::table("Game")->count();
        $current = 0;

        while(true){
            $datas = DB::table("Game")->select()
            ->offset($start*$row)->limit($row)->get();

            $start++;

            foreach ($datas as $key => $data) {
                $data->mysql_id = $data->id;
                unset($data->id);
                $data->description = trim($data->description);

                $data->game_tags_string = explode(",",$data->game_tags_string);
                $data->game_images_string = explode(",",$data->game_images_string);
                $data->game_images_mini_string = explode(",",$data->game_images_mini_string);
                $data->sys_requirements = json_decode($data->sys_requirements);
                $data->soft_requirements = json_decode($data->soft_requirements);

                $size_valid = false;
                
                if(strpos($data->size,"M")> -1){
                    $data->size = str_replace("MB","",$data->size);
                    $data->size = (float)str_replace("M","",$data->size);
                    $size_valid = true;
                }
                if(strpos($data->size,"G")> -1){
                    $data->size = str_replace("GB","",$data->size);
                    $data->size = (float)str_replace("G","",$data->size) * 1000;
                    $size_valid = true;
                }

                if(!$size_valid){
                    $data->size = 0;
                }

                $data->publish_date_by_ali = date(DateTime::ISO8601,strtotime($data->publish_date_by_ali));


                $params = [
                    "index" => "games",
                    "type" => "games",
                    "body" =>  $data 
                ];
                $data = $es->client->index($params);

            }
            $current += count($datas);

            $this->info("{$current}/{$count}");

            if(count($datas) == 0 ){
                return false;
            }
        }

    }
}