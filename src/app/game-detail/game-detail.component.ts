import { Component, ViewChild } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { GameService } from 'app/api/gameService';
import { NgbCarouselConfig } from '@ng-bootstrap/ng-bootstrap';
import { log } from 'util';

@Component({
    selector: 'games',
    templateUrl: './game-detail.component.html',
    styleUrls: ['./game-detail.component.scss'],
})

export class GameDetailComponent {
    @ViewChild('carousel1') carousel1: any;

    gameService:any;
    game_id:string;
    game = {
        name:"",
        version:"",
        game_type:"",
        image_url:"",
        image_alt:"",
        inLanguage:"",
        publisher:"",
        detail_page:"",
        download_page:"",
        description:"",
        install_info:"",
        game_images_mini_string:[],
        game_images_string:"",
        game_tags_string:[],
        game_tags_obj:[],
        sys_requirements:[]
    };
  
    tags_map = [
        {title:"单人单机",icon:"user"},
        {title:"菜鸟入门",icon:"kiwi-bird"},
        {title:"不支持手柄",icon:"keyboard"},
        {title:"支持手柄",icon:"gamepad"},
        {title:"2D画面",icon:"image"},
        {title:"3D画面",icon:"cube"},
        {title:"中级水平",icon:"user-ninja"},
        {title:"冒险",icon:"paw"},
        {title:"RPG",icon:"sword"},
        {title:"解谜",icon:"puzzle-piece"},
    ]

    constructor(
        private route: ActivatedRoute,
        gameService: GameService,
        config: NgbCarouselConfig
    ){
        this.gameService = gameService;
        this.game_id = this.route.snapshot.paramMap.get("id");
        config.interval = 10000;
        config.wrap = false;
        config.keyboard = false;
        config.pauseOnHover = false;
        config.showNavigationArrows = true;
        config.showNavigationIndicators = false;
    }

    ngOnInit() {
        this.gameService.getGameDataById({ id: this.game_id }).subscribe((data) => {
            this.game = data;

            if(this.game.description){
                this.game.description = this.game.description.replace(/\n/g,'<br/>');
            }

            if(this.game.install_info){
                this.game.install_info = this.game.install_info.replace(/\n/g,'<br/>');
            }

            if(this.game.game_tags_string){
                this.game.game_tags_obj = this.game.game_tags_string.map(item=>{
                    return this.getTagIcon(item);
                })
            }
            
        });
    }

    indicatorClick(i){
        this.carousel1.select("ngb-slide-"+i);
    }

    getTagIcon(title:string){
        for (const tag of this.tags_map) {
            if(tag.title == title){
                return tag;
            }
        }
        return this.tags_map[0];
    }
}
