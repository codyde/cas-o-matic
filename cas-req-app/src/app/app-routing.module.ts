import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component'
import { SpcdetailComponent } from './spcdetail/spcdetail.component';
import { RemoveorgComponent } from './removeorg/removeorg.component';
import { OrgdataComponent } from './orgdata/orgdata.component';


const routes: Routes = [
  {path: '', redirectTo: '/home', pathMatch: 'full'},
  { path: 'home', component: HomeComponent }, 
  { path: 'spcdetail', component: SpcdetailComponent },
  { path: 'removeorg', component: RemoveorgComponent },
  { path: 'orgdata', component: OrgdataComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
