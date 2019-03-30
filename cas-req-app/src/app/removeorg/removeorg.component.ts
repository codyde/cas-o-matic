import { Component, ViewChild } from '@angular/core';
import { RestService } from './rest.service';

export interface Token {
  account: string;
}

@Component({
  selector: 'app-removeorg',
  templateUrl: './removeorg.component.html',
  styleUrls: ['./removeorg.component.scss']
})
export class RemoveorgComponent {

  @ViewChild("f") formValues; // Added this
  account: string

  public show:boolean = false;
  public showres:boolean = false;

  res: any = []

  constructor(private rs: RestService) { }

  onSubmit(token: Token) {
    console.log(token)
    this.show = true;
    this.rs.newCall(token).subscribe(result => {
    this.res = result;
    console.log(this.res);
    this.show = false;
    })
  this.formValues.resetForm();
  }

}
