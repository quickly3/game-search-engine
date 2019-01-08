import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { BootstrapModule } from 'app/bootstrap/bootstrap.module';
import { FormsModule } from '@angular/forms';

import { GamesComponent } from './games.component';
import { GamesRoutingModule } from './games-routing.module';


// import { DashboardModule } from './dashboard/dashboard.module';
// import { PagesRoutingModule } from './pages-routing.module';
// import { ThemeModule } from '../@theme/theme.module';

const PAGES_COMPONENTS = [
    GamesComponent,
];

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        GamesRoutingModule,
        BootstrapModule
    ],
    declarations: [
        ...PAGES_COMPONENTS,
    ],
})
export class GamesModule {
}