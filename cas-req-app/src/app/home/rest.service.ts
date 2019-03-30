import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';

const endpoint = 'http://'+window.location.host+'/api/createorg'
const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type':  'application/json'
  })
}

export interface Token {
  account: string;
}

@Injectable({
  providedIn: 'root'
})
export class RestService {

  constructor(private http: HttpClient) { }

  newCall(form){
    return this.http.post(endpoint, form, httpOptions)
  }

}
