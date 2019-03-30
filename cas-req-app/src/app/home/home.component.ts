import { Component, ViewChild } from '@angular/core';
import { Casdata } from './casdata'
import { RestService } from './rest.service'

export interface Token {
  account: string;
}

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  
  @ViewChild("f") formValues; // Added this
  account: string

  public casdata: Casdata = <Casdata>{};

  public show:boolean = false;
  public showres:boolean = false;

  constructor(private rs: RestService) { }

  onSubmit(token: Token) {
    console.log(token);
    this.show = true;
    this.rs.newCall(token).subscribe((data: Casdata) => {
      this.casdata = data;
      this.show = false;
      this.showres = true;
      console.log(this.casdata)
      console.log(data)
    });
    this.formValues.resetForm();
  }

}
