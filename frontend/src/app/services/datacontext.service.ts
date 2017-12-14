import { Injectable } from '@angular/core';
import {Http, Response} from '@angular/http';

@Injectable()
export class DataContextService {

    baseUrl: string = 'http://127.0.0.1:5000'

    constructor(private _http: Http) {

    }

    // 获取样本数目
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

    // 获取样本列表
    getSampleList(): void{
        this._http.get(this.baseUrl + '/sample/action/?action=list&type=all&author=all')
        .subscribe(
            data =>{
                console.log(data.json());
            },
            error =>{
                console.log(error);
            }
        );
    }

    doTest(): void{
        // this.getSampleCount()
        this.getSampleList()
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
