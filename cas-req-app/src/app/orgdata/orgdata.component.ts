import { Component, ViewChild } from '@angular/core';
import { Orgstats } from './orgstats'
import { RestService } from './rest.service'

export interface Token {
  apikey: string;
}

@Component({
  selector: 'app-orgdata',
  templateUrl: './orgdata.component.html',
  styleUrls: ['./orgdata.component.scss']
})
export class OrgdataComponent {

  @ViewChild("f") formValues; // Added this
  apikey: string

    public orgstats: Orgstats = <Orgstats>{};
    public show:boolean = false;
    public showres:boolean = false;

  constructor(private rs: RestService) { }

    onSubmit(token: Token) {
      console.log(token);
      this.show = true;
      this.rs.newCall(token).subscribe((data: Orgstats) => {
        this.orgstats = data;
        this.show = false;
        this.showres = true;
        console.log(this.orgstats)
        console.log(data)
      });
      this.formValues.resetForm();
    }

}
