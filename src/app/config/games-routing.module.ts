import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { GamesComponent } from 'app/component/main/games.component';

const routes: Routes = [
    {
        path: '',
        component: GamesComponent,
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule],
})
export class GamesRoutingModule {
}
