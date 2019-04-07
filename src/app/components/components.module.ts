import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common'; 
import { NavComponent } from './nav/nav.component';

@NgModule({ 
    imports: [ 
        CommonModule 
    ], 
    declarations: [NavComponent],
    exports:[CommonModule,NavComponent] 
}) 

export class ComponentsModule { }