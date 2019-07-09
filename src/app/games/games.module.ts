import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { BootstrapModule } from 'app/plugins/bootstrap.module';
import { FormsModule } from '@angular/forms';

import { GamesComponent } from './games.component';
// import { GamesRoutingModule } from './games-routing.module';
import { AppRoutingModule } from 'app/app-routing.module';
import { ComponentsModule } from '../components/components.module';
import { AngularFontAwesomeModule } from 'angular-font-awesome';


const PAGES_COMPONENTS = [
    GamesComponent,
    // NavComponent
];

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        AppRoutingModule,
        BootstrapModule,
        ComponentsModule,
        AngularFontAwesomeModule
    ],
    declarations: [
        ...PAGES_COMPONENTS,
    ],
})
export class GamesModule {
}