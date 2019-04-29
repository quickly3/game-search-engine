<?php

namespace App\Console\Commands;

use App\User;
use Illuminate\Console\Command;
use DB;
use App\Model\Elastic\ElasticModel;
use App\Services\EscnService;
use DateTime;

class EscnWordCloud extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     * @translator laravelacademy.org
     */
    protected $signature = 'EscnWordCloud';

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
        $words_cloud = EscnService::genWordsCloud();
        dump($words_cloud);
    }

}