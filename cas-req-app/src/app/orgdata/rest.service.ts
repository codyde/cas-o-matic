import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';

const endpoint = 'http://127.0.0.1/api/orgstats'
const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type':  'application/json'
  })
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