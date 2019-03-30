import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';

const endpoint = 'http://127.0.0.1/api/spcorgs'
const deletion = 'http://127.0.0.1/api/deleteorg'

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

  onDelete(account){
    return this.http.post(deletion, account, httpOptions)
  }

  newCall(){
    return this.http.get(endpoint, httpOptions)
  }

}
