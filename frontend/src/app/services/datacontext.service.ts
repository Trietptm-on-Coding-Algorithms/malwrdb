import { Injectable } from '@angular/core';
import {Http, Response} from '@angular/http';

@Injectable()
export class DataContextService {

    baseUrl: string = 'http://127.0.0.1:5000'

    constructor(private _http: Http) {

    }

    getSampleCount(): number{
        this._http.get(this.baseUrl + '/sample/action/?action=count&type=all&author=all')
        .subscribe(
            data =>{
                console.log(data.json());
            },
            error =>{
                console.log(error);
            }
        );
        return 0;
    }

    doTest(): void{
        this.getSampleCount()
    }

    getTestData(): void {
    	this._http.get(this.baseUrl + '/test/?a=1&b=2&c=3')
			.subscribe(data=>{
				console.log(data.json())
			},
			error=>{
				console.log(error)
			}
		);
    }
}
