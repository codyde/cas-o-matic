import { Component, OnInit } from '@angular/core';
import { Spctable } from './spctable'
import { RestService } from './rest.service'
import { ToastrService } from 'ngx-toastr'

export interface Deletion {
  account: string;
}

@Component({
  selector: 'app-spcdetail',
  templateUrl: './spcdetail.component.html',
  styleUrls: ['./spcdetail.component.scss']
})
export class SpcdetailComponent implements OnInit {

  public spcdata: Spctable = <Spctable>{};
  public data: Spctable[];
  public deleteData: Deletion;
  public myString: any;
  public show:boolean = false;

  constructor(private rs: RestService, private toastr: ToastrService) { }
  
  gogo(deleteData){
    this.toastr.success('The account '+deleteData+' is being removed from a SPC Org','',{positionClass: 'toast-bottom-center', enableHtml: true, progressBar: true});
  }

  complete(){
    this.toastr.success('Removal completed successfully','',{positionClass: 'toast-bottom-center', enableHtml: true, progressBar: true});
  }

  onDeletion(account: Deletion){
    this.show = true;
    this.deleteData = account
    this.gogo(this.deleteData)
    this.myString = '{"account":"'+this.deleteData+'"}'
    this.rs.onDelete(JSON.parse(this.myString)).subscribe(result => {
      this.rs.newCall().subscribe(result => {
        this.data = result as Spctable[];
        console.log(this.data)
        this.complete()
        this.show = false;
      }
      )
    })
  }

  ngOnInit() {
    this.rs.newCall().subscribe(result => {
      this.data = result as Spctable[];
      console.log(this.data)
    }
    )
  }
}
