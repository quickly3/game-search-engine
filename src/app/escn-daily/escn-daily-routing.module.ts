import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { EscnDailyComponent } from './escn-daily.component';

const routes: Routes = [
    { path: '',component: EscnDailyComponent,},

];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule],
})
export class EscnDailyRoutingModule {

}
