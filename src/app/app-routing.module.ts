import { ExtraOptions, RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';

import { GamesComponent } from './games/games.component';
import { FanjuComponent } from './fanju/fanju.component';
import { EscnDailyComponent } from './escn-daily/escn-daily.component';
import { GameDetailComponent } from './game-detail/game-detail.component';


const routes: Routes = [
    { path: 'games', component: GamesComponent },
    { path: 'fanju', component: FanjuComponent },
    { path: 'escn-daily', component: EscnDailyComponent },
    { path: 'game-detail/:id', component: GameDetailComponent },
    { path: '', redirectTo: 'fanju', pathMatch: 'full' },
    { path: '**', redirectTo: 'fanju' }
];

const config: ExtraOptions = {
    useHash: true,
    // enableTracing: true
};

@NgModule({
    imports: [RouterModule.forRoot(routes, config)],
    exports: [RouterModule],
})
export class AppRoutingModule {
}
