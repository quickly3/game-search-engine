import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { BootstrapModule } from 'app/plugins/bootstrap.module';

import { AppRoutingModule } from 'app/app-routing.module';
import { GamesComponent } from './games.component';

import { FormsModule } from '@angular/forms';
import { ComponentsModule } from '../components/components.module';
import { AngularFontAwesomeModule } from 'angular-font-awesome';


const PAGES_COMPONENTS = [
    GamesComponent,
];

@NgModule({
    imports: [
        CommonModule,
        AppRoutingModule,
        BootstrapModule,
        FormsModule,
        ComponentsModule,
        AngularFontAwesomeModule
    ],
    declarations: [
        ...PAGES_COMPONENTS,
    ],
})
export class GamesModule {
}