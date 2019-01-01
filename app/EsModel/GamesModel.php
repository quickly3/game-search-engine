<?php

namespace App\EsModel;

use ScoutElastic\Searchable;
use Illuminate\Database\Eloquent\Model;

class GamesModel extends Model
{   
    protected $table = "Game";
    use Searchable;

    /**
     * @var string
     */
    protected $indexConfigurator = \App\EsConfigurator\GamesIndexConfigurator::class;
    protected $index_name = "games";
    /**
     * @var array
     */
    protected $searchRules = [
        //
    ];

    /**
     * @var array
     */
    protected $mapping = [
        "properties"=> [
          "appid"=> [
            "type"=> "long"
          ],
          "conid"=> [
            "type"=> "long"
          ],
          "description"=> [
            "type"=> "text",
            "fields"=> [
              "keyword"=> [
                "type"=> "keyword",
                "ignore_above"=> 256
              ]
            ],
            "analyzer"=> "ik_max_word"
          ],
          "detail_page"=> [
            "type"=> "keyword"
          ],
          "download_page"=> [
            "type"=> "keyword"
          ],
          "game_images_mini_string"=> [
            "type"=> "keyword"
          ],
          "game_images_string"=> [
            "type"=> "keyword"
          ],
          "game_tags_string"=> [
            "type"=> "keyword"
          ],
          "game_type"=> [
            "type"=> "keyword"
          ],
          "image_alt"=> [
            "type"=> "keyword"
          ],
          "image_url"=> [
            "type"=> "keyword"
          ],
          "inLanguage"=> [
            "type"=> "keyword"
          ],
          "install_info"=> [
            "type"=> "text",
            "fields"=> [
              "keyword"=> [
                "type"=> "keyword",
                "ignore_above"=> 256
              ]
            ],
            "analyzer"=> "ik_max_word"
          ],
          "license"=> [
            "type"=> "keyword"
          ],
          "mysql_id"=> [
            "type"=> "long"
          ],
          "name"=> [
            "type"=> "text",
            "fields"=> [
              "keyword"=> [
                "type"=> "keyword",
                "ignore_above"=> 256
              ]
            ],
            "analyzer"=> "ik_max_word"
          ],
          "name_chs"=> [
            "type"=> "text",
            "fields"=> [
              "keyword"=> [
                "type"=> "keyword",
                "ignore_above"=> 256
              ]
            ],
            "analyzer"=> "ik_max_word"
          ],
          "name_en"=> [
            "type"=> "text",
            "fields"=> [
              "keyword"=> [
                "type"=> "keyword",
                "ignore_above"=> 256
              ]
            ]
          ],
          "publish_date_by_ali"=> [
            "type"=> "date"
          ],
          "publisher"=> [
            "type"=> "text",
            "fields"=> [
              "keyword"=> [
                "type"=> "keyword",
                "ignore_above"=> 256
              ]
            ],
            "analyzer"=> "ik_max_word"
          ],
          "size"=> [
            "type"=> "float"
          ],
          "state"=> [
            "type"=> "long"
          ],
          "sys_requirements"=> [
            "properties"=> [
              "key"=> [
                "type"=> "keyword"
              ],
              "v1"=> [
                "type"=> "text",
                "fields"=> [
                  "keyword"=> [
                    "type"=> "keyword",
                    "ignore_above"=> 256
                  ]
                ],
                "analyzer"=> "ik_max_word"
              ],
              "v2"=> [
                "type"=> "text",
                "fields"=> [
                  "keyword"=> [
                    "type"=> "keyword",
                    "ignore_above"=> 256
                  ]
                ],
                "analyzer"=> "ik_max_word"
              ]
            ]
          ],
          "version"=> [
            "type"=> "text",
            "fields"=> [
              "keyword"=> [
                "type"=> "keyword",
                "ignore_above"=> 256
              ]
            ],
            "analyzer"=> "ik_max_word"
          ]
        ]
    ];

    public function toSearchableArray()
    {
        // $array = $this->toArray();

        $_array = [];
        $_array['id'] = $this->id;
        $_array['try_name'] = "try".$this->name;

        return $_array;
    }


    public function searchableAs()
    {
        return 'games';
    }
    
    // public function getScoutKey()
    // {
    //     return $this->mysql_id;
    // }


}