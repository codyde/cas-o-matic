import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ClarityModule } from '@clr/angular';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HomeComponent } from './home/home.component';
import { FormsModule } from "@angular/forms";
import { SpcdetailComponent } from './spcdetail/spcdetail.component';
import { RemoveorgComponent } from './removeorg/removeorg.component';
import { OrgdataComponent } from './orgdata/orgdata.component';
import { ToastrModule } from 'ngx-toastr'


@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    SpcdetailComponent,
    RemoveorgComponent,
    OrgdataComponent
  ],
  imports: [
    BrowserModule,
    ToastrModule.forRoot(),
    AppRoutingModule,
    HttpClientModule,
    ClarityModule,
    BrowserAnimationsModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
