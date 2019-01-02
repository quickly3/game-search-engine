import { ExtraOptions, RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
// import {
//     NbAuthComponent,
//     NbLoginComponent,
//     NbLogoutComponent,
//     NbRegisterComponent,
//     NbRequestPasswordComponent,
//     NbResetPasswordComponent,
// } from '@nebular/auth';

const routes: Routes = [
    { path: 'games', loadChildren: '../modules/main/games.module#GamesModule'},
    { path: '', redirectTo: 'games', pathMatch: 'full' },
    { path: '**', redirectTo: 'games' }
];

const config: ExtraOptions = {
    useHash: true,
    enableTracing: true
};

@NgModule({
    imports: [RouterModule.forRoot(routes, config)],
    exports: [RouterModule],
})
export class AppRoutingModule {
}
