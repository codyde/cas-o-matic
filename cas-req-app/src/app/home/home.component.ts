import { Component, ViewChild } from '@angular/core';
import { Casdata } from './casdata'
import { RestService } from './rest.service'
import { ToastrService } from 'ngx-toastr'


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
  public showbutton:boolean = false;

  constructor(private rs: RestService, private toastr: ToastrService) { }
  
  gogo(casdata){
    this.toastr.success('The account '+casdata.account+' has been added','',{positionClass: 'toast-bottom-center', enableHtml: true, progressBar: true});
  }

  onSubmit(token: Token) {
    console.log(token);
    this.show = true;
    this.rs.newCall(token).subscribe((data: Casdata) => {
      this.casdata = data;
      this.show = false;
      this.showres = true;
      console.log(this.casdata)
      console.log(data)
      this.gogo(this.casdata)
      this.showbutton = true;
    });
    this.formValues.resetForm();
  }

  buildProject() {
    this.rs.createProject(this.casdata).subscribe((ret: any) => {
      console.log(ret)
      this.toastr.success('Default Project Created','',{positionClass: 'toast-bottom-center', enableHtml: true, progressBar: true});
      this.showbutton = false;
    }
    )
  }

}
