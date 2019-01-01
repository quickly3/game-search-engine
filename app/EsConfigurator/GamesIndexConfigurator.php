<?php

namespace App\EsConfigurator;

use ScoutElastic\IndexConfigurator;
use ScoutElastic\Migratable;

class GamesIndexConfigurator extends IndexConfigurator
{
    use Migratable;
    protected $name = 'games';  
    /**
     * @var array
     */
    protected $settings = [
        //
    ];
}