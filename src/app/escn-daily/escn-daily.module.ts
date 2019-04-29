import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { EscnDailyComponent } from './escn-daily.component';
import { EscnDailyRoutingModule } from './escn-daily-routing.module';
import { CommonModule } from '@angular/common';

import { BootstrapModule } from 'app/plugins/bootstrap.module';
import { FormsModule } from '@angular/forms';

import { ComponentsModule } from '../components/components.module';
// import { AngularFontAwesomeModule } from 'angular-font-awesome';


const PAGES_COMPONENTS = [
    EscnDailyComponent,
    // NavComponent
];

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        EscnDailyRoutingModule,
        BootstrapModule,
        ComponentsModule,
        // AngularFontAwesomeModule
    ],
    declarations: [
        ...PAGES_COMPONENTS,
    ],
})
export class EscnDailyModule {
}