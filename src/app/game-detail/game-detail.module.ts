import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { BootstrapModule } from 'app/plugins/bootstrap.module';

import { FormsModule } from '@angular/forms';

// import { GameDetailRoutingModule } from './game-detail-routing.module';
import { AppRoutingModule } from 'app/app-routing.module';
import { GameDetailComponent } from './game-detail.component';
import { AngularFontAwesomeModule } from 'angular-font-awesome';
import { ComponentsModule } from '../components/components.module';


const PAGES_COMPONENTS = [
    GameDetailComponent,
];

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        AppRoutingModule,
        AngularFontAwesomeModule,
        BootstrapModule,
        ComponentsModule
    ],
    declarations: [
        ...PAGES_COMPONENTS,
    ],
})
export class GameDetailModule {
}