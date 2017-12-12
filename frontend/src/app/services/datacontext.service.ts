import { Injectable } from '@angular/core';
import {Http, Response} from '@angular/http';

@Injectable()
export class DataContextService {

    constructor(private _http: Http) {

    }

    getTestData(): void {
    	this._http.get('http://127.0.0.1:5000/test/?a=1&b=2&c=3')
			.subscribe(data=>{
				console.log(data.json())
			},
			error=>{
				console.log(error)
			}
		);
    }
}
