import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { BootstrapModule } from 'app/plugins/bootstrap.module';

import { FormsModule } from '@angular/forms';

import { GameDetailRoutingModule } from './game-detail-routing.module';
import { GameDetailComponent } from './game-detail.component';

const PAGES_COMPONENTS = [
    GameDetailComponent,
];

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        GameDetailRoutingModule,
        BootstrapModule
    ],
    declarations: [
        ...PAGES_COMPONENTS,
    ],
})
export class GameDetailModule {
}