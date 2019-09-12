<?php

namespace App;

use ScoutElastic\IndexConfigurator;
use ScoutElastic\Migratable;

class UserConfigurator extends IndexConfigurator
{
    use Migratable;

    protected $name = 'users';

    /**
     * @var array
     */
    protected $settings = [
        //
    ];
}
