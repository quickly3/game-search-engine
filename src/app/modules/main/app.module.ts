import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from 'app/component/main/app.component';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BootstrapModule } from 'app/modules/bootstrap.module';
import { AppRoutingModule } from 'app/config/app-routing.module';



@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    AppRoutingModule,
    BootstrapModule
  ],
  providers: [

  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
