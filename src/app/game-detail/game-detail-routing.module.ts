import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { GameDetailComponent } from './game-detail.component';

const routes: Routes = [
    { path: '/:id', component: GameDetailComponent, },

];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule],
})
export class GameDetailRoutingModule {

}
